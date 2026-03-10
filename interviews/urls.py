from django.urls import path
from . import views

app_name = 'interviews'

urlpatterns = [
    # Interview rounds
    path('opportunity/<int:opportunity_id>/rounds/', views.interview_rounds_view, name='interview-rounds'),

    # ✅ Fixed: use existing view name
    path('opportunity/<int:opportunity_id>/rounds/create/', views.create_interview_slot_view, name='create-interview-round'),

    # Interview slots
    path('round/<int:round_id>/slots/', views.interview_slots_view, name='interview-slots'),
    path('round/<int:round_id>/slots/create/', views.create_interview_slot_view, name='create-interview-slot'),

    # Assign students to slots
    path('round/<int:round_id>/assign/', views.assign_students_view, name='assign-students'),

    # Feedback
    path('application/<int:application_id>/round/<int:round_id>/feedback/add/', views.add_feedback_view, name='add-feedback'),
    path('application/<int:application_id>/feedback/', views.interview_feedback_view, name='interview-feedback'),
]