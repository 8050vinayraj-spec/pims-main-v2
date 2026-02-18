from django.contrib import admin
from .models import Company, RecruiterProfile, CompanyHistory


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'city', 'verified', 'verified_by', 'created_at')
    list_filter = ('verified', 'industry', 'created_at')
    search_fields = ('name', 'website', 'city')
    readonly_fields = ('created_at', 'updated_at', 'verified_at')


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'designation', 'verified')
    list_filter = ('company', 'verified', 'created_at')
    search_fields = ('user__username', 'company__name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(CompanyHistory)
class CompanyHistoryAdmin(admin.ModelAdmin):
    list_display = ('company', 'past_hires', 'total_applications_received', 'last_hiring_year')
    list_filter = ('last_hiring_year',)
    search_fields = ('company__name',)
    readonly_fields = ('created_at', 'updated_at')

