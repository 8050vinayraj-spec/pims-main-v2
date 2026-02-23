from django.urls import path
from . import views

# Register namespace for reverse lookups
app_name = 'dashboard'

urlpatterns = [
    # Officer dashboard
    path('officer/', views.officer_dashboard_view, name='officer-dashboard'),

    # Recruiter dashboard
    path('recruiter/', views.recruiter_dashboard_view, name='recruiter-dashboard'),

    # Student dashboard
    path('student/', views.student_dashboard_view, name='student-dashboard'),

    # Analytics export
    path('export/', views.analytics_export_view, name='analytics-export'),
]