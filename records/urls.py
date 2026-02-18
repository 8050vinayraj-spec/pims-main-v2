from django.urls import path
from . import views

app_name = 'records'

urlpatterns = [
    path('placements/', views.placement_records_view, name='placement-records'),
    path('reports/', views.placement_reports_view, name='placement-reports'),
    path('student/<int:student_id>/placements/', views.student_placements_view, name='student-placements'),
    path('student/<int:student_id>/placements/add/', views.add_placement_record_view, name='add-placement-record'),
    path('company/<int:company_id>/stats/', views.company_placement_stats_view, name='company-stats'),
]
