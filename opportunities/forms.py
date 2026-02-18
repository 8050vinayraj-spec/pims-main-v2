from django import forms
from .models import Opportunity, RequiredSkill
from students.models import Skill


class OpportunityForm(forms.ModelForm):
	class Meta:
		model = Opportunity
		fields = ('title', 'type', 'description', 'min_cgpa', 'ctc_or_stipend', 'deadline', 'max_applicants')
		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title'}),
			'type': forms.Select(attrs={'class': 'form-select'}),
			'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Role responsibilities, requirements, and benefits'}),
			'min_cgpa': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01, 'min': 0, 'max': 10, 'placeholder': 'e.g., 7.5'}),
			'ctc_or_stipend': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 12 LPA or 50,000/month'}),
			'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'max_applicants': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
		}


class RequiredSkillForm(forms.ModelForm):
	skill = forms.ModelChoiceField(
		queryset=Skill.objects.all().order_by('name'),
		widget=forms.Select(attrs={'class': 'form-select'})
	)

	class Meta:
		model = RequiredSkill
		fields = ('skill', 'proficiency_level')
		widgets = {
			'proficiency_level': forms.Select(attrs={'class': 'form-select'}),
		}


class OpportunityFilterForm(forms.Form):
	search = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search opportunities...'}),
	)
	type = forms.ChoiceField(
		required=False,
		choices=[('', 'All Types')] + Opportunity.OPPORTUNITY_TYPE,
		widget=forms.Select(attrs={'class': 'form-select'}),
	)
	status = forms.ChoiceField(
		required=False,
		choices=[('', 'All Status')] + Opportunity.STATUS,
		widget=forms.Select(attrs={'class': 'form-select'}),
	)
