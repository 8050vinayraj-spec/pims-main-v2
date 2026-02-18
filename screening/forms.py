from django import forms
from .models import ScreeningRule, ScreeningResult


class ScreeningRuleForm(forms.ModelForm):
    class Meta:
        model = ScreeningRule
        fields = ('min_cgpa', 'allowed_branches')
        widgets = {
            'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0, 'max': 10}),
            'allowed_branches': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CSE,ECE,ME (leave blank for all)'}),
        }


class ScreeningResultForm(forms.ModelForm):
    class Meta:
        model = ScreeningResult
        fields = ('result', 'reason')
        widgets = {
            'result': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
