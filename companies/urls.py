from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list_view, name='company_list'),
    path('companies/<int:company_id>/', views.company_detail_view, name='company_detail'),
    path('companies/create/', views.create_company_view, name='create_company'),
    path('companies/<int:company_id>/edit/', views.edit_company_view, name='edit_company'),
    path('companies/verify/', views.officer_verify_company_view, name='officer_verify_company'),
    path('recruiter/dashboard/', views.recruiter_dashboard_view, name='recruiter_dashboard'),
]
