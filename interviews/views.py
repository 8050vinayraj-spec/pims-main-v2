from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q, Max
from students.models import StudentProfile
from opportunities.models import Opportunity
from applications.models import Application
from .models import InterviewRound, InterviewSlot, ApplicationSlotAssignment, InterviewFeedback
from .forms import (
    InterviewRoundForm, InterviewSlotForm, ApplicationSlotAssignmentForm,
    InterviewFeedbackForm, BulkSlotAssignmentForm
)


@login_required
def interview_rounds_view(request, opportunity_id):
    """Create a new interview round"""
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
    # ✅ Check if user is a recruiter from this company
    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters from this company can create rounds.")
    
    if request.method == 'POST':
        form = InterviewRoundForm(request.POST)
        if form.is_valid():
            round = form.save(commit=False)
            round.opportunity = opportunity
            # ✅ Auto-assign next order number
            max_order = InterviewRound.objects.filter(opportunity=opportunity).aggregate(Max('order'))['order__max'] or 0
            round.order = max_order + 1
            round.save()
            messages.success(request, f"Interview round '{round.get_name_display()}' created successfully.")
            return redirect('interviews:interview-rounds', opportunity_id=opportunity.id)
    else:
        form = InterviewRoundForm()
    
    context = {
        'form': form,
        'opportunity': opportunity,
        'page_title': 'Create Interview Round',
    }
    return render(request, 'interviews/create_interview_round.html', context)

@login_required
def interview_slots_view(request, round_id):
    """List interview slots for a round"""
    round = get_object_or_404(InterviewRound, id=round_id)
    opportunity = round.opportunity
    
    # Check if user is recruiter for this company
    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters can view slots.")
    
    slots = round.slots.all()
    
    context = {
        'round': round,
        'opportunity': opportunity,
        'slots': slots,
    }
    return render(request, 'interviews/interview_slots.html', context)


@login_required
def create_interview_slot_view(request, round_id):
    """Create interview slots"""
    round = get_object_or_404(InterviewRound, id=round_id)
    opportunity = round.opportunity
    
    # Check if user is recruiter
    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters can create slots.")
    
    if request.method == 'POST':
        form = InterviewSlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.round = round
            slot.save()
            messages.success(request, f"Interview slot created for {slot.scheduled_at.strftime('%Y-%m-%d %H:%M')}.")
            return redirect('interviews:interview-slots', round_id=round.id)
    else:
        form = InterviewSlotForm()
    
    context = {
        'form': form,
        'round': round,
        'opportunity': opportunity,
        'page_title': 'Create Interview Slot',
    }
    return render(request, 'interviews/create_interview_slot.html', context)


@login_required
def assign_students_view(request, round_id):
    """Assign students to interview slots for a round"""
    round = get_object_or_404(InterviewRound, id=round_id)
    opportunity = round.opportunity
    
    # Check if user is recruiter
    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters can assign.")
    
    # Get unassigned applications that passed previous rounds (if any)
    if round.order == 1:
        # First round: get applications with SHORTLISTED status
        applications = Application.objects.filter(
            opportunity=opportunity,
            status='SHORTLISTED'
        ).exclude(slot_assignment__isnull=False)
    else:
        # Later rounds: get applications that passed previous round feedback
        from django.db.models import Exists, OuterRef
        prev_feedbacks = InterviewFeedback.objects.filter(
            application=OuterRef('pk'),
            round__order=round.order - 1,
            result='PASS'
        )
        applications = Application.objects.filter(
            opportunity=opportunity,
        ).filter(Exists(prev_feedbacks)).exclude(slot_assignment__isnull=False)
    
    # Set choices for the form (needed for both GET and POST)
    application_choices = [
        (app.id, f"{app.student.user.get_full_name()} ({app.student.branch} - Year {app.student.year})")
        for app in applications
    ]
    
    if request.method == 'POST':
        form = BulkSlotAssignmentForm(round_id=round.id, data=request.POST)
        form.fields['applications'].choices = application_choices
        if form.is_valid():
            selected_app_ids = form.cleaned_data['applications']
            slot = form.cleaned_data['slot']
            
            count = 0
            for app_id in selected_app_ids:
                app = get_object_or_404(Application, id=app_id, opportunity=opportunity)
                assignment, created = ApplicationSlotAssignment.objects.get_or_create(
                    application=app,
                    defaults={'slot': slot}
                )
                if created:
                    count += 1
                    slot.status = 'BOOKED'
                    slot.save()
            
            messages.success(request, f"{count} student(s) assigned to interview slot.")
            return redirect('interviews:interview-slots', round_id=round.id)
    else:
        form = BulkSlotAssignmentForm(round_id=round.id)
        form.fields['applications'].choices = application_choices
    
    context = {
        'form': form,
        'round': round,
        'opportunity': opportunity,
        'page_title': 'Assign Students to Slots',
    }
    return render(request, 'interviews/assign_students.html', context)


@login_required
def add_feedback_view(request, application_id, round_id):
    """Add interview feedback for an application in a round"""
    application = get_object_or_404(Application, id=application_id)
    round = get_object_or_404(InterviewRound, id=round_id)
    opportunity = round.opportunity
    
    # Check if user is recruiter
    if request.user.role != 'RECRUITER' or request.user.company != opportunity.company:
        return HttpResponseForbidden("Only recruiters can add feedback.")
    
    # Get or create feedback
    feedback, created = InterviewFeedback.objects.get_or_create(
        application=application,
        round=round
    )
    
    if request.method == 'POST':
        form = InterviewFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, "Interview feedback saved successfully.")
            return redirect('interviews:interview-slots', round_id=round.id)
    else:
        form = InterviewFeedbackForm(instance=feedback)
    
    context = {
        'form': form,
        'application': application,
        'round': round,
        'opportunity': opportunity,
        'page_title': 'Add Interview Feedback',
    }
    return render(request, 'interviews/add_feedback.html', context)


@login_required
def interview_feedback_view(request, application_id):
    """View all interview feedback for an application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Check if user is recruiter or the student
    is_recruiter = request.user.role == 'RECRUITER' and request.user.company == application.opportunity.company
    is_student = StudentProfile.objects.filter(
        user=request.user
    ).filter(user=application.student.user).exists()
    
    if not (is_recruiter or is_student):
        return HttpResponseForbidden("You don't have permission.")
    
    feedbacks = application.interview_feedbacks.all()
    
    context = {
        'application': application,
        'feedbacks': feedbacks,
        'opportunity': application.opportunity,
    }
    return render(request, 'interviews/interview_feedback.html', context)
