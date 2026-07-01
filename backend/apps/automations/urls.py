from django.urls import path
from .views import AdminWorkflowListView, AdminWorkflowDetailView, AdminWorkflowSendsView

urlpatterns = [
    path('admin/workflows/', AdminWorkflowListView.as_view(), name='admin-workflow-list'),
    path('admin/workflows/<str:workflow_id>/', AdminWorkflowDetailView.as_view(), name='admin-workflow-detail'),
    path('admin/workflows/<str:workflow_id>/sends/', AdminWorkflowSendsView.as_view(), name='admin-workflow-sends'),
]
