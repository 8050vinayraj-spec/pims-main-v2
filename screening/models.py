from django.db import models
from applications.models import Application
from students.models import StudentProfile
from opportunities.models import Opportunity


class ScreeningRule(models.Model):
	opportunity = models.OneToOneField(Opportunity, on_delete=models.CASCADE, related_name='screening_rule')
	min_cgpa = models.FloatField(default=0.0)
	allowed_branches = models.CharField(max_length=255, blank=True, help_text='Comma-separated branch codes')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Rules for {self.opportunity.title}"


class ScreeningResult(models.Model):
	RESULT_CHOICES = [
		('ELIGIBLE', 'Eligible'),
		('NOT_ELIGIBLE', 'Not Eligible'),
	]

	application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='screening_result')
	result = models.CharField(max_length=20, choices=RESULT_CHOICES)
	reason = models.TextField(blank=True)
	screened_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.application} - {self.result}"
