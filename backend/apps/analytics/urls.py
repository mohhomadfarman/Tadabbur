from django.urls import path
from .views import AdminOverviewStatsView

urlpatterns = [
    path('admin/overview/', AdminOverviewStatsView.as_view(), name='admin-analytics-overview'),
]
