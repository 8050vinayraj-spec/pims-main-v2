from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.contrib import messages
from companies.models import Company

import csv
import re
from datetime import timedelta
from decimal import Decimal, InvalidOperation

from accounts.models import CustomUser
from students.models import StudentProfile
from opportunities.models import Opportunity
from applications.models import Application
from screening.models import ScreeningResult
from decisions.models import HiringDecision, OfferResponse
from records.models import PlacementRecord

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


def _sync_application_statuses():
    now = timezone.now()
    Application.objects.filter(
        hiring_decision__result='REJECTED'
    ).exclude(status='REJECTED').update(status='REJECTED', updated_at=now)

    Application.objects.filter(
        hiring_decision__result='SELECTED'
    ).exclude(status='SHORTLISTED').update(status='SHORTLISTED', updated_at=now)


def _sync_placements_from_accepted_offers():
    accepted_offers = OfferResponse.objects.filter(
        response='ACCEPTED'
    ).select_related(
        'decision__application__student',
        'decision__application__opportunity__company',
        'decision__application__opportunity'
    )

    for offer in accepted_offers:
        application = offer.decision.application
        placement_date = (offer.responded_at or timezone.now()).date()
        placement_year = placement_date.year
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


@login_required
def officer_dashboard_view(request):
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can access this.")

    _sync_application_statuses()
    _sync_placements_from_accepted_offers()

    total_students = StudentProfile.objects.count()
    total_companies = Company.objects.count()
    total_opportunities = Opportunity.objects.filter(status='PUBLISHED').count()
    total_applications = Application.objects.count()

    placed_students = PlacementRecord.objects.values('student').distinct().count()
    placement_rate = (placed_students / total_students * 100) if total_students > 0 else 0

    pending_companies = Company.objects.filter(verified=False).count()
    pending_recruiters = CustomUser.objects.filter(role='RECRUITER', is_approved=False).count()

    recent_applications = Application.objects.select_related(
        'student', 'opportunity', 'opportunity__company', 'hiring_decision', 'hiring_decision__offer_response'
    ).order_by('-applied_at')[:10]

    avg_package = PlacementRecord.objects.aggregate(avg=Avg('package'))['avg'] or 0

    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_opportunities': total_opportunities,
        'total_applications': total_applications,
        'placed_students': placed_students,
        'placement_rate': placement_rate,
        'pending_companies': pending_companies,
        'pending_recruiters': pending_recruiters,
        'recent_applications': recent_applications,
        'avg_package': avg_package,
    }
    return render(request, 'dashboard/officer_dashboard.html', context)


@login_required
def officer_approval_view(request):
    """Officer view to approve recruiters"""
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can access this.")

    pending_recruiters = CustomUser.objects.filter(role='RECRUITER', is_approved=False)

    context = {
        'pending_recruiters': pending_recruiters,
        'page_title': 'Recruiter Approvals',
    }
    return render(request, 'dashboard/officer_approval.html', context)


@login_required
def verify_company_view(request):
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can access this.")

    companies = Company.objects.filter(verified=False)

    context = {
        'companies': companies,
        'page_title': 'Verify Companies',
    }
    return render(request, 'dashboard/verify_company.html', context)

@login_required
def recruiter_dashboard_view(request):
    user = request.user

    if user.role.upper() != 'RECRUITER':
        messages.error(request, "Only recruiters can access this page.")
        return HttpResponseForbidden("Only recruiters can access this.")

    if not user.is_approved:
        messages.warning(request, "Your recruiter account is not yet approved.")
        return render(request, 'accounts/approval_pending.html')

    company = getattr(user, 'company', None)
    if not company:
        messages.error(request, "No company is associated with your account.")
        return render(request, 'dashboard/no_company_assigned.html')  # Optional: use a template instead of raw 403

    total_opportunities = Opportunity.objects.filter(company=company).count()
    published_opportunities = Opportunity.objects.filter(company=company, status='PUBLISHED').count()
    total_applications = Application.objects.filter(opportunity__company=company).count()
    shortlisted = Application.objects.filter(opportunity__company=company, status='SHORTLISTED').count()
    selected = HiringDecision.objects.filter(application__opportunity__company=company, result='SELECTED').count()
    accepted_offers = OfferResponse.objects.filter(decision__application__opportunity__company=company, response='ACCEPTED').count()

    recent_applications = Application.objects.filter(opportunity__company=company).select_related(
        'student', 'opportunity').order_by('-applied_at')[:10]

    context = {
        'company': company,
        'total_opportunities': total_opportunities,
        'published_opportunities': published_opportunities,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'selected': selected,
        'accepted_offers': accepted_offers,
        'recent_applications': recent_applications,
    }

    return render(request, 'dashboard/recruiter_dashboard.html', context)
@login_required
def student_dashboard_view(request):
    try:
        student = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return HttpResponseForbidden("Only students can access this.")

    applications_qs = Application.objects.filter(student=student).select_related(
        'opportunity', 'opportunity__company'
    ).prefetch_related('hiring_decision__offer_response', 'screening_result', 'slot_assignment')

    applications = list(applications_qs)

    total_applications = len(applications)
    shortlisted = sum(1 for app in applications if app.status == 'SHORTLISTED')
    rejected = sum(1 for app in applications if app.status == 'REJECTED')
    offers_made = sum(1 for app in applications if getattr(app, 'hiring_decision', None) and app.hiring_decision.result == 'SELECTED')

    accepted_offers = 0
    for app in applications:
        decision = getattr(app, 'hiring_decision', None)
        if decision and decision.result == 'SELECTED':
            offer_response = getattr(decision, 'offer_response', None)
            if offer_response and offer_response.response == 'ACCEPTED':
                accepted_offers += 1

    screening_results = ScreeningResult.objects.filter(application__student=student).select_related('application__opportunity')
    eligible = screening_results.filter(result='ELIGIBLE').count()
    not_eligible = screening_results.filter(result='NOT_ELIGIBLE').count()

    placements = PlacementRecord.objects.filter(student=student)

    pending_offers = []
    for app in applications:
        decision = getattr(app, 'hiring_decision', None)
        if decision and decision.result == 'SELECTED':
            offer_response = getattr(decision, 'offer_response', None)
            if not offer_response or offer_response.response not in ['ACCEPTED', 'REJECTED']:
                pending_offers.append(app)

    context = {
        'student': student,
        'applications': applications,
        'total_applications': total_applications,
        'shortlisted': shortlisted,
        'rejected': rejected,
        'offers_made': offers_made,
        'accepted_offers': accepted_offers,
        'eligible': eligible,
        'not_eligible': not_eligible,
        'placements': placements,
        'pending_offers': pending_offers,
        'profile_completion': student.profile_completion_percentage(),
    }
    return render(request, 'dashboard/student_dashboard.html', context)


@login_required
def analytics_export_view(request):
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can export data.")

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="placements.csv"'

    writer = csv.writer(response)
    writer.writerow(['Student Name', 'Roll Number', 'Company', 'Position', 'Package (LPA)', 'Year'])

    records = PlacementRecord.objects.select_related('student', 'company')
    for record in records:
        writer.writerow([
            record.student.user.get_full_name(),
            record.student.roll_number,
            record.company.name,
            record.position,
            record.package,
            record.placement_year,
        ])

    return response  # ✅ This line ensures the view returns a valid HttpResponse