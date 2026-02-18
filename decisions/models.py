from django.db import models
from applications.models import Application


class HiringDecision(models.Model):
    """Final hiring decision for an application"""
    DECISION_CHOICES = [
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
        ('WAITLIST', 'Waitlist'),
    ]

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE,
        related_name='hiring_decision'
    )
    result = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES
    )
    comments = models.TextField(blank=True)
    decided_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-decided_at']

    def __str__(self):
        return f"{self.application.student.user.get_full_name()} - {self.result}"


class OfferResponse(models.Model):
    """Student's response to the hiring decision/offer"""
    RESPONSE_CHOICES = [
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('PENDING', 'Pending'),
    ]

    decision = models.OneToOneField(
        HiringDecision,
        on_delete=models.CASCADE,
        related_name='offer_response'
    )
    response = models.CharField(
        max_length=20,
        choices=RESPONSE_CHOICES,
        default='PENDING'
    )
    responded_at = models.DateTimeField(null=True, blank=True)
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.decision.application.student.user.get_full_name()} - {self.response}"

