from django import forms
from .models import Application


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
