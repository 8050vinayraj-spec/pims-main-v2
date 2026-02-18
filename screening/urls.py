from django.urls import path
from . import views

app_name = 'screening'

urlpatterns = [
    path('opportunity/<int:opportunity_id>/rule/', views.screening_rule_view, name='screening_rule'),
    path('opportunity/<int:opportunity_id>/run/', views.run_screening_view, name='run_screening'),
    path('opportunity/<int:opportunity_id>/results/', views.screening_results_view, name='screening_results'),
]
