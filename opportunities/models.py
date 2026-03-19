from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator
from companies.models import Company
from students.models import Skill


class Opportunity(models.Model):
    OPPORTUNITY_TYPE = [
        ('JOB', 'Full Time Job'),
        ('INTERNSHIP', 'Internship'),
    ]

    STATUS = [
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('CLOSED', 'Closed'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='opportunities')
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE)
    description = models.TextField(default='', blank=True)
    min_cgpa = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    ctc_or_stipend = models.CharField(max_length=255)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='DRAFT')
    max_applicants = models.IntegerField(default=100, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.name}"

    def is_expired(self):
        return now().date() > self.deadline

    def auto_close_if_expired(self):
        if self.status == 'PUBLISHED' and self.is_expired():
            self.status = 'CLOSED'
            self.closed_at = now()
            self.save(update_fields=['status', 'closed_at'])

    # ✅ Helper: check if recruiter can post
    def can_be_posted_by(self, user):
        return (
            user.role == 'RECRUITER'
            and user.company == self.company
            and self.company.verified
        )


# ✅ NEW: Opportunity Approval Model
class OpportunityApproval(models.Model):
    APPROVAL_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    opportunity = models.OneToOneField(Opportunity, on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunity_approvals_given'
    )
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.opportunity.title} - {self.status}"


class RequiredSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='required_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency_level = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES,
        default='BEGINNER'
    )

    class Meta:
        unique_together = ('opportunity', 'skill')

    def __str__(self):
        return f"{self.opportunity.title} - {self.skill.name} ({self.get_proficiency_level_display()})"