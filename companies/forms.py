from django import forms
from .models import Company, RecruiterProfile


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'website', 'description', 'logo', 'city', 'industry')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'About the company'}),
            'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'industry': forms.Select(attrs={'class': 'form-select'}),
        }


class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ('company', 'designation', 'phone')
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Hiring Manager, Recruiter'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }


class CompanyVerificationForm(forms.Form):
    ACTION_CHOICES = [
        ('VERIFY', 'Verify Company'),
        ('REJECT', 'Reject Company'),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect()
    )
    rejection_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Reason for rejection (if applicable)'
        })
    )
