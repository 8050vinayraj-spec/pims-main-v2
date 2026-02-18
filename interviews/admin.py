from django.contrib import admin
from .models import InterviewRound, InterviewSlot, ApplicationSlotAssignment, InterviewFeedback


@admin.register(InterviewRound)
class InterviewRoundAdmin(admin.ModelAdmin):
    list_display = ('opportunity', 'name', 'order', 'duration_minutes', 'created_at')
    list_filter = ('opportunity', 'created_at')
    search_fields = ('opportunity__title', 'name')
    ordering = ('opportunity', 'order')


@admin.register(InterviewSlot)
class InterviewSlotAdmin(admin.ModelAdmin):
    list_display = ('round', 'scheduled_at', 'status', 'location')
    list_filter = ('status', 'scheduled_at')
    search_fields = ('round__opportunity__title', 'location')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ApplicationSlotAssignment)
class ApplicationSlotAssignmentAdmin(admin.ModelAdmin):
    list_display = ('application', 'slot', 'assigned_at')
    list_filter = ('assigned_at', 'slot__round__opportunity')
    search_fields = ('application__student__user__first_name', 'application__student__user__last_name')
    readonly_fields = ('assigned_at',)


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ('application', 'round', 'result', 'rating', 'created_at')
    list_filter = ('result', 'created_at', 'round__opportunity')
    search_fields = ('application__student__user__first_name', 'interviewer_name')
    readonly_fields = ('created_at', 'updated_at')
