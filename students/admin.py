from django.contrib import admin
from .models import StudentProfile, AcademicRecord, Skill, StudentSkill, Resume


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'branch', 'year', 'cgpa', 'phone')
    list_filter = ('branch', 'year', 'cgpa')
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'sgpa')
    list_filter = ('semester', 'sgpa')
    search_fields = ('student__user__username',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)


@admin.register(StudentSkill)
class StudentSkillAdmin(admin.ModelAdmin):
    list_display = ('student', 'skill', 'proficiency', 'years_of_experience')
    list_filter = ('proficiency', 'skill__category')
    search_fields = ('student__user__username', 'skill__name')
    readonly_fields = ('added_at',)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('student', 'version', 'is_current', 'uploaded_at')
    list_filter = ('is_current', 'uploaded_at')
    search_fields = ('student__user__username',)
    readonly_fields = ('uploaded_at',)

