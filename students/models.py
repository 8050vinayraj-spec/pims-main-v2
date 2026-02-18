from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('IT', 'Information Technology'),
        ('EEE', 'Electrical & Electronics Engineering'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    cgpa = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
    year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.branch}"

    def profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.cgpa > 0,
            bool(self.phone),
            bool(self.bio),
            bool(self.profile_image),
            self.academic_records.exists(),
            self.skills.exists(),
            self.resumes.exists(),
        ]
        completed = sum(1 for value in fields if value)
        return int((completed / len(fields)) * 100)


class AcademicRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='academic_records')
    semester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    sgpa = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'semester')
        ordering = ['semester']

    def __str__(self):
        return f"{self.student.user.username} - Sem {self.semester}: {self.sgpa}"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(
        max_length=50,
        choices=[
            ('PROGRAMMING', 'Programming Language'),
            ('FRAMEWORK', 'Framework/Library'),
            ('DATABASE', 'Database'),
            ('TOOL', 'Tool/Software'),
            ('LANGUAGE', 'Language'),
            ('OTHER', 'Other'),
        ],
        default='OTHER'
    )

    def __str__(self):
        return self.name


class StudentSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='BEGINNER')
    years_of_experience = models.FloatField(default=0, validators=[MinValueValidator(0)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'skill')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.student.user.username} - {self.skill.name} ({self.proficiency})"


class Resume(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='resumes')
    file = models.FileField(upload_to='resumes/')
    version = models.IntegerField(default=1)
    is_current = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-version']

    def __str__(self):
        return f"{self.student.user.username} - v{self.version}"

    def save(self, *args, **kwargs):
        # If setting this as current, unset others
        if self.is_current:
            Resume.objects.filter(student=self.student).update(is_current=False)
        super().save(*args, **kwargs)

