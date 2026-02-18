from django.contrib import admin
from .models import Application, ApplicationLog


class ApplicationLogInline(admin.TabularInline):
	model = ApplicationLog
	extra = 0


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
	list_display = ['student', 'opportunity', 'status', 'applied_at']
	list_filter = ['status', 'applied_at']
	search_fields = ['student__user__username', 'opportunity__title']
	inlines = [ApplicationLogInline]


@admin.register(ApplicationLog)
class ApplicationLogAdmin(admin.ModelAdmin):
	list_display = ['application', 'status', 'timestamp']
	list_filter = ['status', 'timestamp']
