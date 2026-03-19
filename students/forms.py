from django import forms
from django.core.validators import RegexValidator
from .models import StudentProfile, AcademicRecord, StudentSkill, Skill, Resume

class StudentProfileForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        required=False,
        validators=[
            RegexValidator(
                regex=r'^\d{1,10}$',
                message='Phone number must contain only digits (max 10 digits)'
            )
        ]
    )
    
    custom_branch = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your branch name',
            'id': 'customBranchInput'
        })
    )

    class Meta:
        model = StudentProfile
        fields = ('cgpa', 'branch', 'custom_branch', 'year', 'country_code', 'phone', 'profile_image', 'bio')
        widgets = {
            'cgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.00001',
                'min': '0',
                'max': '10',
                'placeholder': 'Enter CGPA (e.g., 9.12345)',
                'pattern': r'^\d{1,2}(\.\d{1,5})?$'
            }),
            'branch': forms.Select(attrs={'class': 'form-select', 'id': 'branchSelect'}),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4,
                'placeholder': 'Year of study (1-4)'
            }),
            'country_code': forms.Select(attrs={
                'class': 'form-select'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile number (10 digits)',
                'maxlength': '10',
                'pattern': r'\d{1,10}',
                'inputmode': 'numeric'
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something about yourself'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make CGPA read-only if it's already set (not a new profile)
        if self.instance.pk and self.instance.cgpa > 0:
            self.fields['cgpa'].widget.attrs['readonly'] = True
            self.fields['cgpa'].widget.attrs['disabled'] = True
            self.fields['cgpa'].help_text = 'CGPA cannot be modified once set'
        
        # Show custom_branch field if branch is "OTHER"
        if self.instance.pk and self.instance.branch == 'OTHER':
            self.fields['custom_branch'].widget.attrs['style'] = 'display: block;'
    
    def clean(self):
        cleaned_data = super().clean()
        branch = cleaned_data.get('branch')
        custom_branch = cleaned_data.get('custom_branch')
        
        # Validate that custom_branch is filled if "OTHER" is selected
        if branch == 'OTHER' and not custom_branch:
            raise forms.ValidationError('Please specify your branch when selecting "Other"')
        
        return cleaned_data

class AcademicRecordForm(forms.ModelForm):
    class Meta:
        model = AcademicRecord
        fields = ('semester', 'sgpa')
        widgets = {
            'semester': forms.Select(
                attrs={'class': 'form-select'},
                choices=[(i, f'Semester {i}') for i in range(1, 9)]
            ),
            'sgpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.01,
                'min': 0,
                'max': 10,
                'placeholder': 'SGPA'
            }),
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
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': 0.5,
                'min': 0,
                'placeholder': 'Years of experience'
            }),
        }

class AddSkillForm(forms.Form):
    """Form to add new skill if not in list"""
    skill_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skill name'
        })
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
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': 0.5,
            'placeholder': 'Years'
        })
    )

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('file', 'is_current')
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx'
            }),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }