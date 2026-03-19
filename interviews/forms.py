from django import forms
from django.utils import timezone
from .models import InterviewRound, InterviewSlot, ApplicationSlotAssignment, InterviewFeedback


class InterviewRoundForm(forms.ModelForm):
    """Form to create/edit interview rounds"""
    
    class Meta:
        model = InterviewRound
        fields = ['name', 'description', 'duration_minutes']
        widgets = {
            'name': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter round description'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 15}),
        }


class InterviewSlotForm(forms.ModelForm):
    """Form to create/edit interview slots"""
    
    class Meta:
        model = InterviewSlot
        fields = ['scheduled_at', 'location']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'E.g., Conference Room A, Online, etc.'
            }),
        }
    
    def clean_scheduled_at(self):
        scheduled_at = self.cleaned_data.get('scheduled_at')
        if scheduled_at and scheduled_at < timezone.now():
            raise forms.ValidationError("Slot cannot be scheduled in the past.")
        return scheduled_at


class ApplicationSlotAssignmentForm(forms.ModelForm):
    """Form to assign students to interview slots"""
    
    class Meta:
        model = ApplicationSlotAssignment
        fields = ['slot']
        widgets = {
            'slot': forms.Select(attrs={'class': 'form-select'}),
        }


class InterviewFeedbackForm(forms.ModelForm):
    """Form to record interview feedback"""
    
    class Meta:
        model = InterviewFeedback
        fields = ['interviewer_name', 'comments', 'result', 'rating']
        widgets = {
            'interviewer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of interviewer'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter feedback comments'
            }),
            'result': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 10,
                'type': 'range'
            }),
        }


class BulkSlotAssignmentForm(forms.Form):
    """Form for bulk assigning students to slots"""
    applications = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Select Students",
        required=True
    )
    slot = forms.ModelChoiceField(
        queryset=InterviewSlot.objects.filter(status='AVAILABLE'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Interview Slot",
        required=True
    )
    
    def __init__(self, round_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if round_id:
            self.fields['slot'].queryset = InterviewSlot.objects.filter(
                round_id=round_id,
                status='AVAILABLE'
            )
