from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


ROLE_CHOICES = [
    ('STUDENT', 'Student'),
    ('RECRUITER', 'Recruiter'),
    ('OFFICER', 'Officer'),
]


class CustomUser(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT'
    )
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"


class LoginActivity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='login_activities')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"


class AccountApproval(models.Model):
    APPROVAL_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='account_approval')
    approved_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approvals_given'
    )
    status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rejection_reason = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"

