from django.urls import path
from .views import RegisterView, AdminRegistrationListView, AdminRegistrationDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='event-register'),
    path('admin/registrations/', AdminRegistrationListView.as_view(), name='admin-registration-list'),
    path('admin/registrations/<str:reg_id>/', AdminRegistrationDetailView.as_view(), name='admin-registration-detail'),
]
