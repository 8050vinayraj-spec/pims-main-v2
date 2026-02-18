from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Company, RecruiterProfile, CompanyHistory
from .forms import CompanyForm, RecruiterProfileForm, CompanyVerificationForm
from accounts.models import CustomUser


@login_required
def company_list_view(request):
    """List all companies"""
    companies = Company.objects.all()
    
    # Filter by verification status if provided
    verified_filter = request.GET.get('verified')
    if verified_filter == 'true':
        companies = companies.filter(verified=True)
    elif verified_filter == 'false':
        companies = companies.filter(verified=False)
    
    # Search by name
    search = request.GET.get('search')
    if search:
        companies = companies.filter(name__icontains=search)
    
    context = {
        'companies': companies,
        'search': search,
        'verified_filter': verified_filter,
    }
    
    return render(request, 'companies/company_list.html', context)


@login_required
def company_detail_view(request, company_id):
    """View company details"""
    company = get_object_or_404(Company, id=company_id)
    recruiters = company.recruiters.all()
    
    context = {
        'company': company,
        'recruiters': recruiters,
    }
    
    return render(request, 'companies/company_detail.html', context)


@login_required
def create_company_view(request):
    """Create new company (for recruiters)"""
    if request.user.role != 'RECRUITER':
        messages.error(request, 'Only recruiters can create companies.')
        return redirect('company_list')
    
    # Check if recruiter already has a company profile
    if hasattr(request.user, 'recruiter_profile'):
        messages.info(request, 'You already have a company profile.')
        return redirect('company_detail', company_id=request.user.recruiter_profile.company.id)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            
            # Create company history
            CompanyHistory.objects.create(company=company)
            
            # Create recruiter profile
            RecruiterProfile.objects.create(
                user=request.user,
                company=company,
                designation=request.POST.get('designation', 'Recruiter')
            )
            
            messages.success(request, f'{company.name} created successfully! Pending officer verification.')
            return redirect('company_detail', company_id=company.id)
    else:
        form = CompanyForm()
    
    context = {'form': form}
    return render(request, 'companies/create_company.html', context)


@login_required
def edit_company_view(request, company_id):
    """Edit company details (only company recruiters)"""
    company = get_object_or_404(Company, id=company_id)
    
    # Check if user is a recruiter of this company
    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=company).exists():
        messages.error(request, 'You do not have permission to edit this company.')
        return redirect('company_list')
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company_detail', company_id=company.id)
    else:
        form = CompanyForm(instance=company)
    
    context = {
        'form': form,
        'company': company,
    }
    
    return render(request, 'companies/create_company.html', context)


@login_required
def officer_verify_company_view(request):
    """Officer verification of companies"""
    if request.user.role != 'OFFICER':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        company = get_object_or_404(Company, id=company_id)
        form = CompanyVerificationForm(request.POST)
        
        if form.is_valid():
            action = form.cleaned_data.get('action')
            if action == 'VERIFY':
                company.verified = True
                company.verified_by = request.user
                company.verified_at = now()
                company.save()
                messages.success(request, f'Company {company.name} verified successfully.')
            else:  # REJECT
                # For now, we'll just leave it unverified with a note
                company.verified = False
                company.save()
                messages.info(request, f'Company {company.name} rejected.')
            
            return redirect('officer_verify_company')
    
    # Get unverified and verified companies
    unverified_companies = Company.objects.filter(verified=False)
    verified_companies = Company.objects.filter(verified=True)
    
    context = {
        'unverified_companies': unverified_companies,
        'verified_companies': verified_companies,
    }
    
    return render(request, 'companies/verify_company.html', context)


@login_required
def recruiter_dashboard_view(request):
    """Recruiter dashboard"""
    if request.user.role != 'RECRUITER':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    try:
        recruiter = request.user.recruiter_profile
        company = recruiter.company
    except RecruiterProfile.DoesNotExist:
        return redirect('create_company')
    
    # Get company statistics
    opportunities_count = company.opportunities.count() if hasattr(company, 'opportunities') else 0
    
    context = {
        'recruiter': recruiter,
        'company': company,
        'opportunities_count': opportunities_count,
    }
    
    return render(request, 'companies/recruiter_dashboard.html', context)

