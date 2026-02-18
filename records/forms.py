from django import forms
from .models import PlacementRecord


class PlacementRecordForm(forms.ModelForm):
    """Form to create/view placement records"""
    
    class Meta:
        model = PlacementRecord
        fields = ['company', 'package', 'position', 'placement_year', 'placement_date']
        widgets = {
            'company': forms.Select(attrs={'class': 'form-select'}),
            'package': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'e.g., 12.50 for 12.5 LPA'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Software Engineer'
            }),
            'placement_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2000,
                'max': 2100,
                'placeholder': '2024'
            }),
            'placement_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }


class PlacementFilterForm(forms.Form):
    """Form to filter placement records"""
    company = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by company'
        })
    )
    year = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by year'
        })
    )
    min_package = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Min package (LPA)'
        })
    )
