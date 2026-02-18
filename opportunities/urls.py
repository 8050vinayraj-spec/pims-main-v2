from django.urls import path
from . import views

urlpatterns = [
	path('', views.opportunity_list_view, name='opportunity_list'),
	path('create/', views.create_opportunity_view, name='create_opportunity'),
	path('<int:opportunity_id>/', views.opportunity_detail_view, name='opportunity_detail'),
	path('<int:opportunity_id>/edit/', views.edit_opportunity_view, name='edit_opportunity'),
	path('<int:opportunity_id>/publish/', views.publish_opportunity_view, name='publish_opportunity'),
	path('<int:opportunity_id>/close/', views.close_opportunity_view, name='close_opportunity'),
	path('<int:opportunity_id>/skill/add/', views.add_required_skill_view, name='add_required_skill'),
	path('skill/<int:skill_id>/delete/', views.delete_required_skill_view, name='delete_required_skill'),
]
