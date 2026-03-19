from django.urls import path
from . import views

app_name = 'accounts'  # ✅ Enables namespaced URL reversing like 'accounts:login'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('approval-pending/', views.approval_pending_view, name='approval_pending'),
    path('approvals/', views.officer_approval_view, name='officer_approval'),
    path('delete-account/<int:user_id>/', views.delete_account_view, name='delete_account'),  # ✅ NEW
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('login/', views.login_view, name='login')
]