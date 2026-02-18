from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Application, ApplicationLog
from opportunities.models import Opportunity
from students.models import StudentProfile
from companies.models import RecruiterProfile


@login_required
def apply_view(request, opportunity_id):
	"""Apply to an opportunity (students only)"""
	if request.user.role != 'STUDENT':
		messages.error(request, 'Only students can apply to opportunities.')
		return redirect('opportunity_list')
    
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
	student = get_object_or_404(StudentProfile, user=request.user)
    
	if Application.objects.filter(student=student, opportunity=opportunity).exists():
		messages.info(request, 'You have already applied to this opportunity.')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	if opportunity.status != 'PUBLISHED':
		messages.error(request, 'This opportunity is not open for applications.')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	if request.method == 'POST':
		application = Application.objects.create(student=student, opportunity=opportunity)
		ApplicationLog.objects.create(application=application, status='APPLIED')
		messages.success(request, 'Application submitted successfully!')
		return redirect('opportunity_detail', opportunity_id=opportunity.id)
    
	context = {
		'opportunity': opportunity,
	}
	return render(request, 'applications/confirm_apply.html', context)


@login_required
def withdraw_view(request, application_id):
	"""Withdraw an application (students only)"""
	if request.user.role != 'STUDENT':
		messages.error(request, 'Only students can withdraw applications.')
		return redirect('opportunity_list')
    
	application = get_object_or_404(Application, id=application_id)
	if application.student.user != request.user:
		messages.error(request, 'You do not have permission to withdraw this application.')
		return redirect('opportunity_list')
    
	if request.method == 'POST':
		application.status = 'REJECTED'
		application.save(update_fields=['status'])
		ApplicationLog.objects.create(application=application, status='REJECTED')
		messages.success(request, 'Application withdrawn successfully.')
		return redirect('opportunity_detail', opportunity_id=application.opportunity.id)
    
	context = {
		'application': application,
	}
	return render(request, 'applications/confirm_withdraw.html', context)


@login_required
def applicant_list_view(request, opportunity_id):
	"""Recruiter view of applicants for an opportunity"""
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')
    
	opportunity = get_object_or_404(Opportunity, id=opportunity_id)
	if not RecruiterProfile.objects.filter(user=request.user, company=opportunity.company).exists():
		messages.error(request, 'You do not have permission to view applicants for this opportunity.')
		return redirect('opportunity_list')
    
	applications = Application.objects.filter(opportunity=opportunity).select_related('student__user')
    
	context = {
		'opportunity': opportunity,
		'applications': applications,
	}
	return render(request, 'applications/applicant_list.html', context)


@login_required
def recruiter_applications_view(request):
	"""Recruiter overview of applications across their opportunities"""
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')

	try:
		recruiter = RecruiterProfile.objects.get(user=request.user)
	except RecruiterProfile.DoesNotExist:
		messages.error(request, 'You do not have permission to view this page.')
		return redirect('home')

	opportunities = Opportunity.objects.filter(company=recruiter.company).annotate(
		total_applications=Count('applications'),
		shortlisted_applications=Count('applications', filter=Q(applications__status='SHORTLISTED')),
		rejected_applications=Count('applications', filter=Q(applications__status='REJECTED')),
	).order_by('-created_at')

	context = {
		'opportunities': opportunities,
		'company': recruiter.company,
	}
	return render(request, 'applications/recruiter_applications.html', context)


@login_required
def shortlist_application_view(request, application_id):
	"""Shortlist an application (recruiters only)"""
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')
	
	application = get_object_or_404(Application, id=application_id)
	
	# Check if recruiter belongs to the company
	if not RecruiterProfile.objects.filter(user=request.user, company=application.opportunity.company).exists():
		messages.error(request, 'You do not have permission to modify this application.')
		return redirect('opportunity_list')
	
	application.status = 'SHORTLISTED'
	application.save(update_fields=['status'])
	ApplicationLog.objects.create(application=application, status='SHORTLISTED')
	
	messages.success(request, f'{application.student.user.get_full_name()} has been shortlisted.')
	return redirect('applications:applicant_list', opportunity_id=application.opportunity.id)


@login_required
def reject_application_view(request, application_id):
	"""Reject an application (recruiters only)"""
	if request.user.role != 'RECRUITER':
		messages.error(request, 'You do not have access to this page.')
		return redirect('home')
	
	application = get_object_or_404(Application, id=application_id)
	
	# Check if recruiter belongs to the company
	if not RecruiterProfile.objects.filter(user=request.user, company=application.opportunity.company).exists():
		messages.error(request, 'You do not have permission to modify this application.')
		return redirect('opportunity_list')
	
	application.status = 'REJECTED'
	application.save(update_fields=['status'])
	ApplicationLog.objects.create(application=application, status='REJECTED')
	
	messages.info(request, f'{application.student.user.get_full_name()} has been rejected.')
	return redirect('applications:applicant_list', opportunity_id=application.opportunity.id)
