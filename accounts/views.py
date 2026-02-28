from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, LoginActivity, AccountApproval
from .forms import SignupForm, LoginForm, ApprovalActionForm
from students.models import StudentProfile

# ---------------- Signup ----------------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')  # ✅ namespaced

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'STUDENT'
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
        approval_id = request.POST.get('approval_id')
        approval = get_object_or_404(AccountApproval, id=approval_id)
        form = ApprovalActionForm(request.POST)

        if form.is_valid():
            action = form.cleaned_data.get('action')
            if action == 'APPROVE':
                approval.status = 'APPROVED'
                approval.approved_by = request.user
                approval.save()
                approval.user.is_approved = True
                approval.user.save(update_fields=['is_approved'])
                messages.success(request, f"User {approval.user.username} approved successfully.")
            elif action == 'REJECT':
                approval.status = 'REJECTED'
                approval.rejection_reason = form.cleaned_data.get('rejection_reason', '')
                approval.approved_by = request.user
                approval.save()
                approval.user.is_approved = False
                approval.user.save(update_fields=['is_approved'])
                messages.info(request, f"User {approval.user.username} rejected.")

            return redirect('accounts:officer_approval')  # ✅ namespaced

    context = {
        'pending_approvals': AccountApproval.objects.filter(status='PENDING'),
        'approved_approvals': AccountApproval.objects.filter(status='APPROVED'),
        'rejected_approvals': AccountApproval.objects.filter(status='REJECTED'),
    }
    return render(request, 'accounts/approval_list.html', context)

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