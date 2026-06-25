from django.urls import path
from .views import RegisterView, LoginView, TokenRefreshView, ProfileView
from .admin_views import (
    AdminUserListView, AdminUserDetailView, AdminUserPasswordView,
    AdminUserActivityView, RoleListView, RoleDetailView, SectionListView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='auth-token-refresh'),
    path('profile/', ProfileView.as_view(), name='auth-profile'),

    # Admin panel — user management (section: users)
    path('admin/users/', AdminUserListView.as_view(), name='admin-user-list'),
    path('admin/users/<str:user_id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/users/<str:user_id>/password/', AdminUserPasswordView.as_view(), name='admin-user-password'),
    path('admin/users/<str:user_id>/activity/', AdminUserActivityView.as_view(), name='admin-user-activity'),

    # Admin panel — roles & permissions (section: roles)
    path('admin/roles/', RoleListView.as_view(), name='admin-role-list'),
    path('admin/roles/<str:role_id>/', RoleDetailView.as_view(), name='admin-role-detail'),
    path('admin/sections/', SectionListView.as_view(), name='admin-section-list'),
]
