from django.urls import path
from . import views
from .views import CompanyListView, CompanyDetailView

app_name = 'companies'

urlpatterns = [
    path('list/', CompanyListView.as_view(), name='company_list'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('create/', views.create_company_view, name='create_company'),
    path('<int:company_id>/edit/', views.edit_company_view, name='edit_company'),

    # Officer dashboard view
    path('verify/', views.officer_verify_company_view, name='officer_verify_company'),

    # Recruiter dashboard
    path('recruiter/dashboard/', views.recruiter_dashboard_view, name='recruiter_dashboard'),

    # Verify/Reject actions
    path('verify/<int:company_id>/', views.verify_company_view, name='verify_company'),
    path('reject/<int:company_id>/', views.reject_company_view, name='reject_company'),
]