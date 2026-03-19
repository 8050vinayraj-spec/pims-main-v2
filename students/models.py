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
        ('OTHER', 'Other (Please specify)'),
    ]

    COUNTRY_CODES = [
        ('+1', '+1 (United States)'),
        ('+44', '+44 (United Kingdom)'),
        ('+91', '+91 (India)'),
        ('+86', '+86 (China)'),
        ('+81', '+81 (Japan)'),
        ('+33', '+33 (France)'),
        ('+49', '+49 (Germany)'),
        ('+39', '+39 (Italy)'),
        ('+34', '+34 (Spain)'),
        ('+61', '+61 (Australia)'),
        ('+64', '+64 (New Zealand)'),
        ('+27', '+27 (South Africa)'),
        ('+55', '+55 (Brazil)'),
        ('+52', '+52 (Mexico)'),
        ('+1-888', '+1-888 (Canada)'),
        ('+65', '+65 (Singapore)'),
        ('+60', '+60 (Malaysia)'),
        ('+66', '+66 (Thailand)'),
        ('+62', '+62 (Indonesia)'),
        ('+63', '+63 (Philippines)'),
        ('+82', '+82 (South Korea)'),
        ('+84', '+84 (Vietnam)'),
        ('+90', '+90 (Turkey)'),
        ('+966', '+966 (Saudi Arabia)'),
        ('+971', '+971 (United Arab Emirates)'),
        ('+212', '+212 (Morocco)'),
        ('+234', '+234 (Nigeria)'),
        ('+254', '+254 (Kenya)'),
        ('+56', '+56 (Chile)'),
        ('+54', '+54 (Argentina)'),
        ('+57', '+57 (Colombia)'),
        ('+51', '+51 (Peru)'),
        ('+48', '+48 (Poland)'),
        ('+31', '+31 (Netherlands)'),
        ('+32', '+32 (Belgium)'),
        ('+41', '+41 (Switzerland)'),
        ('+43', '+43 (Austria)'),
        ('+46', '+46 (Sweden)'),
        ('+47', '+47 (Norway)'),
        ('+45', '+45 (Denmark)'),
        ('+358', '+358 (Finland)'),
        ('+353', '+353 (Ireland)'),
        ('+30', '+30 (Greece)'),
        ('+36', '+36 (Hungary)'),
        ('+420', '+420 (Czech Republic)'),
        ('+421', '+421 (Slovakia)'),
        ('+203', '+203 (Egypt)'),
        ('+216', '+216 (Tunisia)'),
        ('+213', '+213 (Algeria)'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    cgpa = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    custom_branch = models.CharField(max_length=100, blank=True, help_text='Enter your branch if "Other" is selected')
    year = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(4)]
    )
    country_code = models.CharField(max_length=10, choices=COUNTRY_CODES, default='+91', blank=True)
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

