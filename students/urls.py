from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('academic-records/', views.academic_records_view, name='academic_records'),
    path('academic-records/add/', views.add_academic_record_view, name='add_academic_record'),
    path('academic-records/<int:record_id>/edit/', views.edit_academic_record_view, name='edit_academic_record'),
    path('academic-records/<int:record_id>/delete/', views.delete_academic_record_view, name='delete_academic_record'),
    path('skills/', views.skills_view, name='skills'),
    path('skills/add/', views.add_skill_view, name='add_skill'),
    path('skills/<int:skill_id>/delete/', views.delete_skill_view, name='delete_skill'),
    path('resumes/', views.resumes_view, name='resumes'),
    path('resumes/upload/', views.upload_resume_view, name='upload_resume'),
    path('resumes/<int:resume_id>/delete/', views.delete_resume_view, name='delete_resume'),
    path('resumes/<int:resume_id>/set-current/', views.set_current_resume_view, name='set_current_resume'),
]
