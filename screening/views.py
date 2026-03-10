from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ScreeningRule, ScreeningResult
from .forms import ScreeningRuleForm, ScreeningResultForm
from opportunities.models import Opportunity
from applications.models import Application
from companies.models import RecruiterProfile


def _user_can_manage_screening(user, opportunity):
	"""
	Check if a user has permission to manage screening for an opportunity.
	Allow access if:
	1. User has a RecruiterProfile for the company, OR
	2. User's company field matches the opportunity's company
	"""
	if RecruiterProfile.objects.filter(user=user, company=opportunity.company).exists():
		return True
	if user.company and user.company == opportunity.company:
		return True
	return False


def _matches_rule(student, rule):
	if student.cgpa < rule.min_cgpa:
		return False, f"CGPA below {rule.min_cgpa}"
	if rule.allowed_branches:
		allowed = [b.strip().upper() for b in rule.allowed_branches.split(',') if b.strip()]
		if student.branch.upper() not in allowed:
			return False, "Branch not allowed"
	return True, ""


@login_required
def screening_rule_view(request, opportunity_id):
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')

	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
	if not _user_can_manage_screening(request.user, opportunity):
		messages.error(request, 'You do not have permission to manage screening for this opportunity.')
		return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

	rule, _ = ScreeningRule.objects.get_or_create(opportunity=opportunity)

	if request.method == 'POST':
		form = ScreeningRuleForm(request.POST, instance=rule)
		if form.is_valid():
			form.save()
			messages.success(request, 'Screening rules updated successfully!')
			return redirect('screening:screening_rule', opportunity_id=opportunity.id)
	else:
		form = ScreeningRuleForm(instance=rule)

	context = {
		'form': form,
		'opportunity': opportunity,
	}
	return render(request, 'screening/screening_rule.html', context)


@login_required
def run_screening_view(request, opportunity_id):
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')

	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
	if not _user_can_manage_screening(request.user, opportunity):
		messages.error(request, 'You do not have permission to run screening for this opportunity.')
		return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

	rule = get_object_or_404(ScreeningRule, opportunity=opportunity)
	applications = Application.objects.filter(opportunity=opportunity).select_related('student')

	for application in applications:
		if hasattr(application, 'screening_result'):
			continue
		eligible, reason = _matches_rule(application.student, rule)
		ScreeningResult.objects.create(
			application=application,
			result='ELIGIBLE' if eligible else 'NOT_ELIGIBLE',
			reason=reason
		)

	messages.success(request, 'Screening completed successfully!')
	return redirect('screening:screening_results', opportunity_id=opportunity.id)


@login_required
def screening_results_view(request, opportunity_id):
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')

	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
	if not _user_can_manage_screening(request.user, opportunity):
		messages.error(request, 'You do not have permission to view screening results for this opportunity.')
		return redirect('opportunities:opportunity_detail', opportunity_id=opportunity.id)

	results = ScreeningResult.objects.filter(application__opportunity=opportunity).select_related('application__student__user')

	context = {
		'opportunity': opportunity,
		'results': results,
	}
	return render(request, 'screening/screening_results.html', context)
