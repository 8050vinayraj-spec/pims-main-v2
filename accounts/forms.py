from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ROLE_CHOICES


class SignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address'
        })
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    captcha = forms.CharField(
        label='Security Verification - What is 5 + 3?',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the answer',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'role', 'password1', 'password2', 'captcha')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
    
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if captcha and captcha.strip() != '8':
            raise forms.ValidationError("Incorrect answer. Please try again.")
        return captcha


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    captcha = forms.CharField(
        label='Security Verification - What is 3 + 7?',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the answer',
            'autocomplete': 'off'
        })
    )
    
    def clean_captcha(self):
        captcha = self.cleaned_data.get('captcha')
        if captcha and captcha.strip() != '10':
            raise forms.ValidationError("Incorrect answer. Please try again.")
        return captcha


class ApprovalActionForm(forms.Form):
    ACTION_CHOICES = [
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
    ]
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.RadioSelect()
    )
    company = forms.ModelChoiceField(
        queryset=None,  # Will be set in __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        help_text='Assign company to recruiter (required for recruiter approval)'
    )
    rejection_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Reason for rejection (if applicable)'
        })
    )
    
    def __init__(self, *args, is_recruiter=False, **kwargs):
        super().__init__(*args, **kwargs)
        from companies.models import Company
        self.fields['company'].queryset = Company.objects.all()
        self.is_recruiter = is_recruiter
        
        # Make company required only for recruiters
        if is_recruiter:
            self.fields['company'].required = True
        else:
            self.fields['company'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        action = cleaned_data.get('action')
        company = cleaned_data.get('company')
        
        # If approving a recruiter, company must be selected
        if action == 'APPROVE' and self.is_recruiter and not company:
            raise forms.ValidationError(
                "Company must be assigned when approving a recruiter."
            )
        
        return cleaned_data