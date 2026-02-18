from django.db import models
from django.core.validators import URLValidator
from accounts.models import CustomUser


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    website = models.URLField(validators=[URLValidator()])
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    industry = models.CharField(
        max_length=100,
        choices=[
            ('IT', 'Information Technology'),
            ('FINANCE', 'Finance'),
            ('CONSULTING', 'Consulting'),
            ('MANUFACTURING', 'Manufacturing'),
            ('HEALTHCARE', 'Healthcare'),
            ('RETAIL', 'Retail'),
            ('TELECOMMUNICATIONS', 'Telecommunications'),
            ('OTHER', 'Other'),
        ],
        default='IT'
    )
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_companies'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RecruiterProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='recruiter_profile')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='recruiters')
    designation = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company.name}"


class CompanyHistory(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='history')
    past_hires = models.IntegerField(default=0)
    total_applications_received = models.IntegerField(default=0)
    last_hiring_year = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Company Histories'

    def __str__(self):
        return f"{self.company.name} - {self.past_hires} hires"

