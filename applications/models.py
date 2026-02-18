from django.db import models
from students.models import StudentProfile
from opportunities.models import Opportunity


class Application(models.Model):
	STATUS_CHOICES = [
		('APPLIED', 'Applied'),
		('SHORTLISTED', 'Shortlisted'),
		('REJECTED', 'Rejected'),
	]

	student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
	opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPLIED')
	applied_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		unique_together = ('student', 'opportunity')
		ordering = ['-applied_at']

	def __str__(self):
		return f"{self.student.user.username} - {self.opportunity.title}"


class ApplicationLog(models.Model):
	application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='logs')
	status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
	timestamp = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return f"{self.application} - {self.status}"
