from django.contrib import admin
from .models import HiringDecision, OfferResponse


@admin.register(HiringDecision)
class HiringDecisionAdmin(admin.ModelAdmin):
    list_display = ('application', 'result', 'decided_at')
    list_filter = ('result', 'decided_at')
    search_fields = ('application__student__user__first_name', 'application__student__user__last_name')
    readonly_fields = ('decided_at', 'updated_at')


@admin.register(OfferResponse)
class OfferResponseAdmin(admin.ModelAdmin):
    list_display = ('decision', 'response', 'responded_at')
    list_filter = ('response', 'responded_at')
    search_fields = ('decision__application__student__user__first_name',)
    readonly_fields = ('created_at', 'updated_at')

