from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.opportunity_list_view, name='opportunity_list'),
    path('<int:opportunity_id>/', views.opportunity_detail_view, name='opportunity_detail'),
    path('create/', views.create_opportunity_view, name='create_opportunity'),
    path('<int:opportunity_id>/edit/', views.edit_opportunity_view, name='edit_opportunity'),
    path('<int:opportunity_id>/publish/', views.publish_opportunity_view, name='publish_opportunity'),
    path('<int:opportunity_id>/close/', views.close_opportunity_view, name='close_opportunity'),
    path('<int:opportunity_id>/add-skill/', views.add_required_skill_view, name='add_required_skill'),
    path('delete-skill/<int:skill_id>/', views.delete_required_skill_view, name='delete_required_skill'),
]