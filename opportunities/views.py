from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import Opportunity, RequiredSkill
from .forms import OpportunityForm, RequiredSkillForm, OpportunityFilterForm
from companies.models import RecruiterProfile


@login_required
def opportunity_list_view(request):
	"""List all opportunities"""
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
	"""View opportunity details"""
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


@login_required
def create_opportunity_view(request):
	"""Create new opportunity (recruiters only)"""
	if request.user.role != 'RECRUITER':
		messages.error(request, 'Only recruiters can create opportunities.')
		return redirect('opportunity_list')
    
	try:
		recruiter = request.user.recruiter_profile
		company = recruiter.company
	except RecruiterProfile.DoesNotExist:
		messages.error(request, 'You need a company profile to create opportunities.')
		return redirect('create_company')
    
	if not company.verified:
		messages.warning(request, 'Your company must be verified before posting opportunities.')
		return redirect('dashboard:recruiter-dashboard')
    
	if request.method == 'POST':
		form = OpportunityForm(request.POST)
		if form.is_valid():
			opportunity = form.save(commit=False)
			opportunity.company = company
			opportunity.status = 'DRAFT'
			opportunity.save()
			messages.success(request, 'Opportunity created in draft mode.')
			return redirect('opportunity_detail', opportunity_id=opportunity.id)
	else:
		form = OpportunityForm()
    
	context = {
		'form': form,
		'opportunity': None,
	}
	return render(request, 'opportunities/create_opportunity.html', context)


@login_required
def edit_opportunity_view(request, opportunity_id):
	"""Edit opportunity (recruiters only)"""
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
	if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to edit this opportunity.')
		return redirect('opportunity_list')
    
	if request.method == 'POST':
		form = OpportunityForm(request.POST, instance=opportunity)
		if form.is_valid():
			form.save()
			messages.success(request, 'Opportunity updated successfully!')
			return redirect('opportunity_detail', opportunity_id=opportunity.id)
	else:
		form = OpportunityForm(instance=opportunity)
    
	context = {
		'form': form,
		'opportunity': opportunity,
	}
    
	return render(request, 'opportunities/create_opportunity.html', context)


@login_required
def publish_opportunity_view(request, opportunity_id):
	"""Publish opportunity (change from draft to published)"""
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
	if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to publish this opportunity.')
		return redirect('opportunity_list')
    
	if opportunity.status != 'DRAFT':
		messages.error(request, 'Only draft opportunities can be published.')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	opportunity.status = 'PUBLISHED'
	opportunity.published_at = now()
	opportunity.save()
    
	messages.success(request, f'Opportunity "{opportunity.title}" published successfully!')
	return redirect('opportunity_detail', opportunity_id=opportunity.id)


@login_required
def close_opportunity_view(request, opportunity_id):
	"""Close opportunity (stop accepting applications)"""
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
	if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to close this opportunity.')
		return redirect('opportunity_list')
    
	if request.method == 'POST':
		opportunity.status = 'CLOSED'
		opportunity.closed_at = now()
		opportunity.save()
		messages.success(request, 'Opportunity closed successfully!')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	context = {'opportunity': opportunity}
	return render(request, 'opportunities/confirm_close_opportunity.html', context)


@login_required
def add_required_skill_view(request, opportunity_id):
	"""Add required skill to opportunity"""
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
	if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to edit this opportunity.')
		return redirect('opportunity_list')
    
	if request.method == 'POST':
		form = RequiredSkillForm(request.POST)
		if form.is_valid():
			skill_instance = form.save(commit=False)
			skill_instance.opportunity = opportunity
			skill_instance.save()
			messages.success(request, 'Skill requirement added!')
			return redirect('opportunity_detail', opportunity_id=opportunity.id)
	else:
		form = RequiredSkillForm()
    
	context = {
		'form': form,
		'opportunity': opportunity,
	}
    
	return render(request, 'opportunities/add_required_skill.html', context)


@login_required
def delete_required_skill_view(request, skill_id):
	"""Remove required skill from opportunity"""
	skill = get_object_or_404(RequiredSkill, id=skill_id)
	opportunity = skill.opportunity
    
	if request.user.role != 'RECRUITER' or not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to modify this opportunity.')
		return redirect('opportunity_list')
    
	if request.method == 'POST':
		skill.delete()
		messages.success(request, 'Skill requirement removed!')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	context = {'skill': skill, 'opportunity': opportunity}
	return render(request, 'opportunities/confirm_delete_skill.html', context)
