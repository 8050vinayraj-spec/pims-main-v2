from django.db import models
from students.models import StudentProfile
from companies.models import Company


class PlacementRecord(models.Model):
    """Immutable record of student placements"""
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='placement_records'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='placement_records'
    )
    package = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Annual salary or total package in LPA"
    )
    position = models.CharField(max_length=100)
    placement_year = models.IntegerField(help_text="Year of placement (e.g., 2024)")
    placement_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-placement_date']
        unique_together = ('student', 'company', 'placement_year')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.company.name} ({self.placement_year})"

