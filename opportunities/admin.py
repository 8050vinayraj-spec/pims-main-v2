from django.contrib import admin
from .models import Opportunity, RequiredSkill


class RequiredSkillInline(admin.TabularInline):
	model = RequiredSkill
	extra = 1


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
	list_display = ['title', 'company', 'type', 'status', 'deadline', 'published_at']
	list_filter = ['status', 'type']
	search_fields = ['title', 'company__name']
	readonly_fields = ['created_at', 'updated_at', 'published_at', 'closed_at']
	inlines = [RequiredSkillInline]


@admin.register(RequiredSkill)
class RequiredSkillAdmin(admin.ModelAdmin):
	list_display = ['skill', 'opportunity']
	search_fields = ['skill__name', 'opportunity__title']
