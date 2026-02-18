from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('officer/', views.officer_dashboard_view, name='officer-dashboard'),
    path('recruiter/', views.recruiter_dashboard_view, name='recruiter-dashboard'),
    path('student/', views.student_dashboard_view, name='student-dashboard'),
    path('export/', views.analytics_export_view, name='analytics-export'),
]
