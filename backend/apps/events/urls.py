from django.urls import path
from .views import (
    RegisterView, AdminRegistrationListView, AdminRegistrationDetailView, LaunchSettingsView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='event-register'),
    path('settings/', LaunchSettingsView.as_view(), name='event-settings'),
    path('admin/registrations/', AdminRegistrationListView.as_view(), name='admin-registration-list'),
    path('admin/registrations/<str:reg_id>/', AdminRegistrationDetailView.as_view(), name='admin-registration-detail'),
]
