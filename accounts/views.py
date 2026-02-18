from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, LoginActivity, AccountApproval
from .forms import SignupForm, LoginForm, ApprovalActionForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_approved = False
            user.save()
            
            # Create approval record
            AccountApproval.objects.create(user=user, status='PENDING')
            
            messages.success(request, 'Account created successfully! Awaiting approval from officer.')
            return redirect('approval_pending')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.is_approved:
                    messages.warning(request, 'Your account is pending approval. Please wait.')
                    return redirect('approval_pending')
                
                login(request, user)
                LoginActivity.objects.create(user=user)
                
                # Redirect by role
                if user.role == 'OFFICER':
                    return redirect('dashboard:officer-dashboard')
                elif user.role == 'RECRUITER':
                    return redirect('dashboard:recruiter-dashboard')
                else:  # STUDENT
                    return redirect('dashboard:student-dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('login')


def approval_pending_view(request):
    if request.user.is_authenticated and request.user.is_approved:
        return redirect('home')
    
    return render(request, 'accounts/approval_pending.html')


@login_required
def officer_approval_view(request):
    if request.user.role != 'OFFICER':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        approval_id = request.POST.get('approval_id')
        approval = get_object_or_404(AccountApproval, id=approval_id)
        form = ApprovalActionForm(request.POST)
        
        if form.is_valid():
            action = form.cleaned_data.get('action')
            if action == 'APPROVE':
                approval.status = 'APPROVED'
                approval.user.is_approved = True
                approval.approved_by = request.user
                approval.save()
                approval.user.save()
                messages.success(request, f"User {approval.user.username} approved successfully.")
            else:  # REJECT
                approval.status = 'REJECTED'
                approval.rejection_reason = form.cleaned_data.get('rejection_reason', '')
                approval.approved_by = request.user
                approval.save()
                messages.info(request, f"User {approval.user.username} rejected.")
            
            return redirect('officer_approval')
    
    # Get pending approvals
    pending_approvals = AccountApproval.objects.filter(status='PENDING')
    approved_approvals = AccountApproval.objects.filter(status='APPROVED')
    rejected_approvals = AccountApproval.objects.filter(status='REJECTED')
    
    context = {
        'pending_approvals': pending_approvals,
        'approved_approvals': approved_approvals,
        'rejected_approvals': rejected_approvals,
    }
    
    return render(request, 'accounts/approval_list.html', context)


@login_required
def home_view(request):
    """Redirect to appropriate dashboard based on role"""
    if request.user.role == 'OFFICER':
        return redirect('dashboard:officer-dashboard')
    elif request.user.role == 'RECRUITER':
        return redirect('dashboard:recruiter-dashboard')
    else:  # STUDENT
        return redirect('dashboard:student-dashboard')

