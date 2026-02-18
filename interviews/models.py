from django.db import models
from opportunities.models import Opportunity
from applications.models import Application
from django.utils import timezone


class InterviewRound(models.Model):
    """Represents interview rounds for an opportunity"""
    ROUND_CHOICES = [
        ('TECHNICAL', 'Technical Round'),
        ('HR', 'HR Round'),
        ('MANAGER', 'Manager Round'),
        ('GROUP_DISCUSSION', 'Group Discussion'),
        ('FINAL', 'Final Round'),
    ]

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='interview_rounds'
    )
    name = models.CharField(max_length=50, choices=ROUND_CHOICES)
    order = models.PositiveIntegerField(help_text="Order of the round (1, 2, 3...)")
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['opportunity', 'order']
        unique_together = ('opportunity', 'order')

    def __str__(self):
        return f"{self.opportunity.title} - {self.get_name_display()} (Round {self.order})"


class InterviewSlot(models.Model):
    """Available time slots for interviews"""
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BOOKED', 'Booked'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    round = models.ForeignKey(
        InterviewRound,
        on_delete=models.CASCADE,
        related_name='slots'
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='AVAILABLE'
    )
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['round', 'scheduled_at']

    def __str__(self):
        return f"{self.round} - {self.scheduled_at.strftime('%Y-%m-%d %H:%M')}"

    def is_past(self):
        """Check if slot is in the past"""
        return self.scheduled_at < timezone.now()


class ApplicationSlotAssignment(models.Model):
    """Assignment of students to interview slots"""
    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='slot_assignment'
    )
    slot = models.ForeignKey(
        InterviewSlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_applications'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('application', 'slot')

    def __str__(self):
        return f"{self.application.student.user.get_full_name()} - {self.slot}"


class InterviewFeedback(models.Model):
    """Feedback for each interview slot/round"""
    RESULT_CHOICES = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('HOLD', 'Hold'),
        ('NOT_ATTEMPTED', 'Not Attempted'),
    ]

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='interview_feedbacks'
    )
    round = models.ForeignKey(
        InterviewRound,
        on_delete=models.CASCADE,
        related_name='feedbacks'
    )
    interviewer_name = models.CharField(max_length=255)
    comments = models.TextField(blank=True)
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='NOT_ATTEMPTED'
    )
    rating = models.PositiveIntegerField(
        default=0,
        help_text="Rating out of 10"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('application', 'round')

    def __str__(self):
        return f"{self.application.student.user.get_full_name()} - {self.round.name} - {self.result}"
