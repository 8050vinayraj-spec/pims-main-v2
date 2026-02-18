from django.contrib import admin
from .models import ScreeningRule, ScreeningResult


@admin.register(ScreeningRule)
class ScreeningRuleAdmin(admin.ModelAdmin):
	list_display = ['opportunity', 'min_cgpa', 'allowed_branches']
	search_fields = ['opportunity__title']


@admin.register(ScreeningResult)
class ScreeningResultAdmin(admin.ModelAdmin):
	list_display = ['application', 'result', 'screened_at']
	list_filter = ['result', 'screened_at']
