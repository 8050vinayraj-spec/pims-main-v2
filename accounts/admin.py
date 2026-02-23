from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LoginActivity, AccountApproval

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_approved', 'is_staff')
    list_filter = ('role', 'is_approved', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'is_approved')}),
    )

@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp')
    list_filter = ('timestamp',)
    readonly_fields = ('user', 'timestamp')

@admin.register(AccountApproval)
class AccountApprovalAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'approved_by', 'created_at')
    list_filter = ('status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        approved = (obj.status == 'APPROVED')
        obj.user.is_approved = approved
        obj.user.save(update_fields=['is_approved'])
        print(f"💾 Admin save_model fired for {obj.user.username}: is_approved={approved}")