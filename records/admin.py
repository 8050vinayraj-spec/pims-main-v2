from django.contrib import admin
from .models import PlacementRecord


@admin.register(PlacementRecord)
class PlacementRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'package', 'position', 'placement_year', 'placement_date')
    list_filter = ('placement_year', 'company', 'placement_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'company__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'placement_date'

