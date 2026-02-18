from django import forms
from .models import HiringDecision, OfferResponse


class HiringDecisionForm(forms.ModelForm):
    """Form to record hiring decisions"""
    
    class Meta:
        model = HiringDecision
        fields = ['result', 'comments']
        widgets = {
            'result': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter decision comments'
            }),
        }


class OfferResponseForm(forms.ModelForm):
    """Form for students to respond to job offers"""
    
    class Meta:
        model = OfferResponse
        fields = ['response', 'comments']
        widgets = {
            'response': forms.Select(attrs={'class': 'form-select'}),
            'comments': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional comments'
            }),
        }
