from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from .models import Company, CompanyHistory
from .forms import CompanyForm
from accounts.models import CustomUser


class CompanyListView(ListView):
    model = Company
    template_name = 'companies/company_list.html'
    context_object_name = 'companies'

    def get_queryset(self):
        queryset = super().get_queryset()
        verified_filter = self.request.GET.get('verified')
        search = self.request.GET.get('search')

        if verified_filter == 'true':
            queryset = queryset.filter(verified=True)
        elif verified_filter == 'false':
            queryset = queryset.filter(verified=False)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['verified_filter'] = self.request.GET.get('verified', '')
        return context


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/company_detail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # show recruiters linked via CustomUser
        context['recruiters'] = CustomUser.objects.filter(company=self.object, role='RECRUITER')
        return context


@login_required
def create_company_view(request):
    if request.user.role != 'RECRUITER':
        messages.error(request, 'Only recruiters can create companies.')
        return redirect('companies:company_list')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            CompanyHistory.objects.create(company=company)

            # ✅ Link recruiter directly to the company
            request.user.company = company
            request.user.save()

            messages.success(request, f'{company.name} created successfully! Pending officer verification.')
            return redirect('companies:company_detail', pk=company.id)
    else:
        form = CompanyForm()

    return render(request, 'companies/create_company.html', {'form': form})


@login_required
def edit_company_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)

    # ✅ Check recruiter is linked to this company
    if request.user.role != 'RECRUITER' or request.user.company != company:
        messages.error(request, 'You do not have permission to edit this company.')
        return redirect('companies:company_list')

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('companies:company_detail', pk=company.id)
    else:
        form = CompanyForm(instance=company)

    return render(request, 'companies/create_company.html', {'form': form, 'company': company})


@login_required
def officer_verify_company_view(request):
    if request.user.role != 'OFFICER':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    unverified_companies = Company.objects.filter(verified=False)
    verified_companies = Company.objects.filter(verified=True)

    return render(request, 'companies/verify_company.html', {
        'unverified_companies': unverified_companies,
        'verified_companies': verified_companies,
    })


@require_POST
@login_required
def verify_company_view(request, company_id):
    if request.user.role != 'OFFICER':
        messages.error(request, 'Unauthorized access.')
        return redirect('companies:officer_verify_company')

    company = get_object_or_404(Company, id=company_id)
    company.verified = True
    company.verified_by = request.user
    company.verified_at = now()
    company.save()
    messages.success(request, f'{company.name} has been verified.')
    return redirect('companies:officer_verify_company')


@require_POST
@login_required
def reject_company_view(request, company_id):
    if request.user.role != 'OFFICER':
        messages.error(request, 'Unauthorized access.')
        return redirect('companies:officer_verify_company')

    company = get_object_or_404(Company, id=company_id)
    company.delete()
    messages.info(request, f'{company.name} has been rejected and removed.')
    return redirect('companies:officer_verify_company')


@login_required
def recruiter_dashboard_view(request):
    if request.user.role != 'RECRUITER':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')

    company = request.user.company
    opportunities_count = company.opportunities.count() if company and hasattr(company, 'opportunities') else 0

    return render(request, 'companies/recruiter_dashboard.html', {
        'company': company,
        'opportunities_count': opportunities_count,
    })