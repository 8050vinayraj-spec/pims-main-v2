from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, LoginActivity, AccountApproval
from .forms import SignupForm, LoginForm, ApprovalActionForm
from students.models import StudentProfile
from companies.models import Company, RecruiterProfile

# ---------------- Signup ----------------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  # ✅ namespaced

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')  # ✅ FIXED: Use user's selected role, not hardcoded STUDENT
            user.is_approved = False
            user.save()
            AccountApproval.objects.create(user=user, status='PENDING')
            messages.success(request, 'Account created successfully! Awaiting officer approval.')
            return redirect('accounts:approval_pending')  # ✅ namespaced
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})

# ---------------- Login ----------------

def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  # ✅ namespaced

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_approved:
                    messages.warning(request, 'Your account is pending approval. Please wait.')
                    return redirect('accounts:approval_pending')  # ✅ namespaced

                login(request, user)
                LoginActivity.objects.create(user=user)

                if user.role.upper() == 'OFFICER':
                    return redirect('dashboard:officer-dashboard')
                elif user.role.upper() == 'RECRUITER':
                    return redirect('dashboard:recruiter-dashboard')
                elif user.role.upper() == 'STUDENT':
                    try:
                        _ = user.student_profile
                        return redirect('dashboard:student-dashboard')
                    except StudentProfile.DoesNotExist:
                        messages.info(request, "Please complete your profile before accessing the dashboard.")
                        return redirect('students:complete_profile')
                else:
                    messages.error(request, 'Invalid role assigned to user.')
                    return redirect('accounts:login')  # ✅ namespaced
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# ---------------- Logout ----------------



def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # ✅ Use the correct namespace

# ---------------- Approval Pending ----------------

def approval_pending_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  # ✅ namespaced
    return render(request, 'accounts/approval_pending.html')

# ---------------- Officer Approval ----------------

@login_required
def officer_approval_view(request):
    if request.user.role.upper() != 'OFFICER':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('accounts:home')  # ✅ namespaced

    if request.method == 'POST':
        # Handle account approval
        if 'approval_id' in request.POST:
            approval_id = request.POST.get('approval_id')
            approval = get_object_or_404(AccountApproval, id=approval_id)
            
            is_recruiter = approval.user.role.upper() == 'RECRUITER'
            form = ApprovalActionForm(request.POST, is_recruiter=is_recruiter)

            if form.is_valid():
                action = form.cleaned_data.get('action')
                if action == 'APPROVE':
                    approval.status = 'APPROVED'
                    approval.approved_by = request.user
                    approval.save()
                    approval.user.is_approved = True
                    
                    if is_recruiter:
                        company = form.cleaned_data.get('company')
                        if company:
                            approval.user.company = company
                            RecruiterProfile.objects.get_or_create(
                                user=approval.user,
                                company=company,
                                defaults={'designation': 'Recruiter'}
                            )
                    
                    approval.user.save()
                    messages.success(request, f"User {approval.user.username} approved successfully." + 
                        (f" Assigned to {form.cleaned_data.get('company').name}." if is_recruiter else ""))
                elif action == 'REJECT':
                    approval.status = 'REJECTED'
                    approval.rejection_reason = form.cleaned_data.get('rejection_reason', '')
                    approval.approved_by = request.user
                    approval.save()
                    approval.user.is_approved = False
                    approval.user.save(update_fields=['is_approved'])
                    messages.info(request, f"User {approval.user.username} rejected.")

            return redirect('accounts:officer_approval')
        
        # ✅ NEW: Handle company approval
        elif 'company_approval_id' in request.POST:
            from companies.models import CompanyApproval
            from django.utils.timezone import now as tz_now
            
            company_approval_id = request.POST.get('company_approval_id')
            company_approval = get_object_or_404(CompanyApproval, id=company_approval_id)
            action = request.POST.get('action')
            
            if action == 'APPROVE':
                company_approval.status = 'APPROVED'
                company_approval.approved_by = request.user
                company = company_approval.company
                company.verified = True
                company.verified_by = request.user
                company.verified_at = tz_now()
                company.save()
                company_approval.save()
                messages.success(request, f"Company '{company.name}' verified successfully.")
            elif action == 'REJECT':
                company_approval.status = 'REJECTED'
                company_approval.rejection_reason = request.POST.get('rejection_reason', '')
                company_approval.approved_by = request.user
                company_approval.save()
                messages.info(request, f"Company verification rejected.")
            
            return redirect('accounts:officer_approval')
        
        # ✅ NEW: Handle opportunity approval
        elif 'opportunity_approval_id' in request.POST:
            from opportunities.models import OpportunityApproval
            from django.utils.timezone import now as tz_now
            
            opportunity_approval_id = request.POST.get('opportunity_approval_id')
            opportunity_approval = get_object_or_404(OpportunityApproval, id=opportunity_approval_id)
            action = request.POST.get('action')
            
            if action == 'APPROVE':
                opportunity_approval.status = 'APPROVED'
                opportunity_approval.approved_by = request.user
                opportunity = opportunity_approval.opportunity
                opportunity.status = 'PUBLISHED'
                opportunity.published_at = tz_now()
                opportunity.save()
                opportunity_approval.save()
                messages.success(request, f"Opportunity '{opportunity.title}' published successfully.")
            elif action == 'REJECT':
                opportunity_approval.status = 'REJECTED'
                opportunity_approval.rejection_reason = request.POST.get('rejection_reason', '')
                opportunity_approval.approved_by = request.user
                opportunity_approval.save()
                messages.info(request, f"Opportunity was rejected.")
            
            return redirect('accounts:officer_approval')

# ✅ FIXED: Separate pending approvals by role
    pending_all = AccountApproval.objects.filter(status='PENDING')
    pending_recruiters = pending_all.filter(user__role='RECRUITER')
    pending_students = pending_all.filter(user__role='STUDENT')
    
    # ✅ NEW: Get company approvals
    from companies.models import CompanyApproval
    pending_companies = CompanyApproval.objects.filter(status='PENDING')
    approved_companies = CompanyApproval.objects.filter(status='APPROVED')
    rejected_companies = CompanyApproval.objects.filter(status='REJECTED')
    
    # ✅ NEW: Get opportunity approvals
    from opportunities.models import OpportunityApproval
    pending_opportunities = OpportunityApproval.objects.filter(status='PENDING')
    approved_opportunities = OpportunityApproval.objects.filter(status='APPROVED')
    rejected_opportunities = OpportunityApproval.objects.filter(status='REJECTED')
    
    context = {
        # Account approvals
        'pending_recruiters': pending_recruiters,
        'pending_students': pending_students,
        'pending_approvals': pending_all,
        'approved_approvals': AccountApproval.objects.filter(status='APPROVED'),
        'rejected_approvals': AccountApproval.objects.filter(status='REJECTED'),
        # Company approvals
        'pending_companies': pending_companies,
        'approved_companies': approved_companies,
        'rejected_companies': rejected_companies,
        # Opportunity approvals
        'pending_opportunities': pending_opportunities,
        'approved_opportunities': approved_opportunities,
        'rejected_opportunities': rejected_opportunities,
        # Other
        'companies': Company.objects.all(),
    }
    return render(request, 'accounts/approval_list.html', context)

# ✅ NEW: Delete Account (Officer only)
@login_required
def delete_account_view(request, user_id):
    """Allow officers to delete approved accounts"""
    if request.user.role.upper() != 'OFFICER':
        messages.error(request, 'You do not have permission to delete accounts.')
        return redirect('accounts:home')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        email = user.email
        user.delete()
        messages.success(request, f'Account "{username}" ({email}) has been deleted successfully.')
        return redirect('accounts:officer_approval')
    
    # GET request - show confirmation page
    context = {
        'user': user,
        'confirmation_needed': True
    }
    return render(request, 'accounts/delete_account_confirm.html', context)

# ---------------- Home ----------------

@login_required
def home_view(request):
    if request.user.role.upper() == 'OFFICER':
        return redirect('dashboard:officer-dashboard')
    elif request.user.role.upper() == 'RECRUITER':
        return redirect('dashboard:recruiter-dashboard')
    elif request.user.role.upper() == 'STUDENT':
        try:
            _ = request.user.student_profile
            return redirect('dashboard:student-dashboard')
        except StudentProfile.DoesNotExist:
            return redirect('students:complete_profile')
    else:
        messages.error(request, 'Invalid role assigned to user.')
        return redirect('accounts:login')  # ✅ namespaced