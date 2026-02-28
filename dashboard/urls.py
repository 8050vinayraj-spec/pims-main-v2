from django.urls import path
from . import views

app_name = 'dashboard'  # This is critical for namespacing

urlpatterns = [
    path('officer/', views.officer_dashboard_view, name='officer-dashboard'),
    path('officer/verify-company/', views.verify_company_view, name='officer_verify_company'),
    path('officer/approvals/', views.officer_approval_view, name='officer_approval'),  # ✅ Add this line
    path('recruiter/', views.recruiter_dashboard_view, name='recruiter-dashboard'),
    path('student/', views.student_dashboard_view, name='student-dashboard'),
    path('export/', views.analytics_export_view, name='analytics-export'),
]