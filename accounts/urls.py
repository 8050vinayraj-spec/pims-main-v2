from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('approval-pending/', views.approval_pending_view, name='approval_pending'),
    path('approvals/', views.officer_approval_view, name='officer_approval'),
    path('', views.home_view, name='home'),
]
