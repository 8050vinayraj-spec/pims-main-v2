from django.urls import path
from . import views

app_name = 'decisions'

urlpatterns = [
    path('opportunity/<int:opportunity_id>/', views.decision_list_view, name='decision-list'),
    path('application/<int:application_id>/decision/add/', views.add_hiring_decision_view, name='add-hiring-decision'),
    path('decision/<int:decision_id>/', views.decision_detail_view, name='decision-detail'),
    path('decision/<int:decision_id>/response/', views.offer_response_view, name='offer-response'),
]
