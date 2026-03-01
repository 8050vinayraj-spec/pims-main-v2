from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from django import forms
from .models import Opportunity, RequiredSkill
from .forms import OpportunityForm, RequiredSkillForm, OpportunityFilterForm
from companies.models import RecruiterProfile, Company

# Step 1: Add a form to choose company
class CompanyChoiceForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.none(),
        label="Select Company",
        empty_label="Choose a company",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

@login_required
def opportunity_list_view(request):
    opportunities = Opportunity.objects.filter(status='PUBLISHED').select_related('company')
    closed_any = False
    for opp in opportunities:
        before_status = opp.status
        opp.auto_close_if_expired()
        if before_status != opp.status:
            closed_any = True
    if closed_any:
        opportunities = Opportunity.objects.filter(status='PUBLISHED').select_related('company')

    filter_form = OpportunityFilterForm(request.GET or None)

    if filter_form.is_valid():
        search = filter_form.cleaned_data.get('search')
        opp_type = filter_form.cleaned_data.get('type')
        status = filter_form.cleaned_data.get('status')

        if search:
            opportunities = opportunities.filter(title__icontains=search)
        if opp_type:
            opportunities = opportunities.filter(type=opp_type)
        if status:
            opportunities = opportunities.filter(status=status)
    else:
        search = ''
        opp_type = ''
        status = ''

    context = {
        'opportunities': opportunities,
        'filter_form': filter_form,
        'search': search,
        'opp_type': opp_type,
        'status': status,
    }

    return render(request, 'opportunities/opportunity_list.html', context)


@login_required
def opportunity_detail_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    opportunity.auto_close_if_expired()
    opportunity.refresh_from_db()
    required_skills = opportunity.required_skills.all()
    today = now().date()
    days_left = (opportunity.deadline - today).days if opportunity.deadline > today else 0
    can_manage = False
    student_application = None

    if request.user.role == 'RECRUITER':
        can_manage = RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists()
    if request.user.role == 'STUDENT':
        from applications.models import Application
        student_application = Application.objects.filter(
            student__user=request.user,
            opportunity=opportunity
        ).first()

    context = {
        'opportunity': opportunity,
        'required_skills': required_skills,
        'is_expired': opportunity.is_expired(),
        'days_left': days_left,
        'can_manage': can_manage,
        'student_application': student_application,
    }

    return render(request, 'opportunities/opportunity_detail.html', context)


# Step 2: Updated view to support company selection
@login_required
def create_opportunity_view(request):
    if request.user.role != 'RECRUITER':
        messages.error(request, 'Only recruiters can create opportunities.')
        return redirect('opportunities:opportunity_list')

    recruiter_profiles = RecruiterProfile.objects.filter(user=request.user, verified=True)
    verified_companies = [rp.company for rp in recruiter_profiles]

    if not verified_companies:
        messages.error(request, 'You need a verified company profile to create opportunities.')
        return redirect('companies:create_company')

    if request.method == 'POST':
        company_form = CompanyChoiceForm(request.POST)
        company_form.fields['company'].queryset = Company.objects.filter(id__in=[c.id for c in verified_companies])
        form = OpportunityForm(request.POST)

        if company_form.is_valid() and form.is_valid():
            company = company_form.cleaned_data['company']
            opportunity = form.save(commit=False)
            opportunity.company = company
            opportunity.status = 'DRAFT'
            opportunity.save()
            messages.success(request, 'Opportunity created in draft mode.')
            return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)
    else:
        company_form = CompanyChoiceForm()
        company_form.fields['company'].queryset = Company.objects.filter(id__in=[c.id for c in verified_companies])
        form = OpportunityForm()

    return render(request, 'opportunities/create_opportunity.html', {
        'form': form,
        'company_form': company_form,
        'opportunity': None
    })


@login_required
def edit_opportunity_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
        messages.error(request, 'You do not have permission to edit this opportunity.')
        return redirect('opportunities:opportunity_list')

    if request.method == 'POST':
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated successfully!')
            return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)
    else:
        form = OpportunityForm(instance=opportunity)

    return render(request, 'opportunities/create_opportunity.html', {'form': form, 'opportunity': opportunity})


@login_required
def publish_opportunity_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
        messages.error(request, 'You do not have permission to publish this opportunity.')
        return redirect('opportunities:opportunity_list')

    if opportunity.status != 'DRAFT':
        messages.error(request, 'Only draft opportunities can be published.')
        return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

    opportunity.status = 'PUBLISHED'
    opportunity.published_at = now()
    opportunity.save()

    messages.success(request, f'Opportunity "{opportunity.title}" published successfully!')
    return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)


@login_required
def close_opportunity_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
        messages.error(request, 'You do not have permission to close this opportunity.')
        return redirect('opportunities:opportunity_list')

    if request.method == 'POST':
        opportunity.status = 'CLOSED'
        opportunity.closed_at = now()
        opportunity.save()
        messages.success(request, 'Opportunity closed successfully!')
        return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

    return render(request, 'opportunities/confirm_close_opportunity.html', {'opportunity': opportunity})


@login_required
def add_required_skill_view(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
        messages.error(request, 'You do not have permission to edit this opportunity.')
        return redirect('opportunities:opportunity_list')

    if request.method == 'POST':
        form = RequiredSkillForm(request.POST)
        if form.is_valid():
            skill_instance = form.save(commit=False)
            skill_instance.opportunity = opportunity
            skill_instance.save()
            messages.success(request, 'Skill requirement added!')
            return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)
    else:
        form = RequiredSkillForm()

    return render(request, 'opportunities/add_required_skill.html', {'form': form, 'opportunity': opportunity})


@login_required
def delete_required_skill_view(request, skill_id):
    skill = get_object_or_404(RequiredSkill, id=skill_id)
    opportunity = skill.opportunity

    if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
        messages.error(request, 'You do not have permission to modify this opportunity.')
        return redirect('opportunities:opportunity_list')

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill requirement removed!')
        return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

    return render(request, 'opportunities/confirm_delete_skill.html', {'skill': skill, 'opportunity': opportunity})