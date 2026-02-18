from django import forms
from .models import StudentProfile, AcademicRecord, StudentSkill, Skill, Resume


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('cgpa', 'branch', 'year', 'phone', 'profile_image', 'bio')
        widgets = {
            'cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0, 'max': 10}),
            'branch': forms.Select(attrs={'class': 'form-select'}),
            'year': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'Year {i}') for i in range(1, 5)]),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile number'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'About yourself'}),
        }


class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ('semester', 'sgpa')
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-select'}, choices=[(i, f'Semester {i}') for i in range(1, 9)]),
            'sgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0, 'max': 10, 'placeholder': 'SGPA'}),
        }


class StudentSkillForm(forms.ModelForm):
    skill = forms.ModelChoiceField(
        queryset=Skill.objects.all().order_by('name'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Select Skill'
    )

    class Meta:
        model = StudentSkill
        fields = ('skill', 'proficiency', 'years_of_experience')
        widgets = {
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.5, 'min': 0, 'placeholder': 'Years'}),
        }


class AddSkillForm(forms.Form):
    """Form to add new skill if not in list"""
    skill_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter skill name'})
    )
    category = forms.ChoiceField(
        choices=[
            ('PROGRAMMING', 'Programming Language'),
            ('FRAMEWORK', 'Framework/Library'),
            ('DATABASE', 'Database'),
            ('TOOL', 'Tool/Software'),
            ('LANGUAGE', 'Language'),
            ('OTHER', 'Other'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    proficiency = forms.ChoiceField(
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced'),
            ('EXPERT', 'Expert'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    years_of_experience = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': 0.5, 'placeholder': 'Years'})
    )


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('file', 'is_current')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
