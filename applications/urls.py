from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:opportunity_id>/', views.apply_view, name='apply'),
    path('withdraw/<int:application_id>/', views.withdraw_view, name='withdraw_application'),
    path('opportunity/<int:opportunity_id>/applicants/', views.applicant_list_view, name='applicant_list'),
    path('recruiter/', views.recruiter_applications_view, name='recruiter_applications'),
    path('application/<int:application_id>/shortlist/', views.shortlist_application_view, name='shortlist_application'),
    path('application/<int:application_id>/reject/', views.reject_application_view, name='reject_application'),
]
