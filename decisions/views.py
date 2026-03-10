from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import re

from companies.models import Company
from students.models import StudentProfile
from applications.models import Application, ApplicationLog
from records.models import PlacementRecord
from .models import HiringDecision, OfferResponse
from .forms import HiringDecisionForm, OfferResponseForm


def _parse_package(ctc_or_stipend):
    if not ctc_or_stipend:
        return Decimal('0.00')
    match = re.search(r"\d+(?:\.\d+)?", str(ctc_or_stipend))
    if not match:
        return Decimal('0.00')
    try:
        return Decimal(match.group(0))
    except InvalidOperation:
        return Decimal('0.00')


@login_required
def decision_list_view(request, opportunity_id):
    from opportunities.models import Opportunity
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)

    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters can view decisions.")

    applications = Application.objects.filter(
        opportunity=opportunity
    ).select_related('hiring_decision')

    context = {
        'opportunity': opportunity,
        'applications': applications,
    }
    return render(request, 'decisions/decision_list.html', context)


@login_required
def add_hiring_decision_view(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.user.role != 'RECRUITER' or request.user.company != application.opportunity.company:
        return HttpResponseForbidden("Only recruiters can make decisions.")

    decision, created = HiringDecision.objects.get_or_create(application=application)

    if request.method == 'POST':
        form = HiringDecisionForm(request.POST, instance=decision)
        if form.is_valid():
            decision = form.save()
            if decision.result == 'REJECTED' and application.status != 'REJECTED':
                application.status = 'REJECTED'
                application.save(update_fields=['status', 'updated_at'])
                ApplicationLog.objects.create(application=application, status='REJECTED')
            elif decision.result == 'SELECTED' and application.status != 'SHORTLISTED':
                application.status = 'SHORTLISTED'
                application.save(update_fields=['status', 'updated_at'])
                ApplicationLog.objects.create(application=application, status='SHORTLISTED')
            messages.success(request, f"Hiring decision recorded: {decision.get_result_display()}")
            return redirect('decisions:decision-list', opportunity_id=application.opportunity.id)
    else:
        form = HiringDecisionForm(instance=decision)

    context = {
        'form': form,
        'application': application,
        'opportunity': application.opportunity,
        'page_title': 'Add Hiring Decision',
    }
    return render(request, 'decisions/add_hiring_decision.html', context)


@login_required
def offer_response_view(request, decision_id):
    decision = get_object_or_404(HiringDecision, id=decision_id)
    application = decision.application

    is_student = StudentProfile.objects.filter(
        user=request.user
    ).filter(user=application.student.user).exists()
    is_recruiter = request.user.role == 'RECRUITER' and request.user.company == application.opportunity.company

    if not (is_student or is_recruiter):
        return HttpResponseForbidden("You don't have permission.")

    response, created = OfferResponse.objects.get_or_create(decision=decision)

    if request.method == 'POST':
        if not is_student:
            return HttpResponseForbidden("Only students can respond to offers.")

        form = OfferResponseForm(request.POST, instance=response)
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.response != 'PENDING':
                obj.responded_at = timezone.now()
            obj.save()
            if obj.response == 'ACCEPTED':
                placement_year = timezone.now().year
                placement_date = timezone.now().date()
                package = _parse_package(application.opportunity.ctc_or_stipend)
                PlacementRecord.objects.get_or_create(
                    student=application.student,
                    company=application.opportunity.company,
                    placement_year=placement_year,
                    defaults={
                        'package': package,
                        'position': application.opportunity.title,
                        'placement_date': placement_date,
                    }
                )
            messages.success(request, f"Offer response submitted: {obj.get_response_display()}")
            return redirect('dashboard:student-dashboard')
    else:
        form = OfferResponseForm(instance=response)

    context = {
        'form': form,
        'decision': decision,
        'application': application,
        'opportunity': application.opportunity,
        'is_student': is_student,
        'page_title': 'Respond to Offer',
    }
    return render(request, 'decisions/offer_response.html', context)


@login_required
def decision_detail_view(request, decision_id):
    decision = get_object_or_404(HiringDecision, id=decision_id)
    application = decision.application

    is_student = StudentProfile.objects.filter(
        user=request.user
    ).filter(user=application.student.user).exists()
    is_recruiter = request.user.role == 'RECRUITER' and request.user.company == application.opportunity.company

    if not (is_student or is_recruiter):
        return HttpResponseForbidden("You don't have permission.")

    offer_response = getattr(decision, 'offer_response', None)

    context = {
        'decision': decision,
        'application': application,
        'opportunity': application.opportunity,
        'offer_response': offer_response,
        'is_student': is_student,
        'is_recruiter': is_recruiter,
    }
    return render(request, 'decisions/decision_detail.html', context)


@login_required
def verify_company_view(request):
    """Officer view to verify companies"""
    if request.user.role.upper() != 'OFFICER':
        messages.error(request, 'You do not have access to this page.')
        return redirect('dashboard:officer-dashboard')

    companies = Company.objects.filter(is_verified=False)

    context = {
        'companies': companies,
        'page_title': 'Verify Companies',
    }
    return render(request, 'dashboard/verify_company.html', context)