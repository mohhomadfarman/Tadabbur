from django.urls import path
from .views import AdminOverviewStatsView, AdminTrackStatsView

urlpatterns = [
    path('admin/overview/', AdminOverviewStatsView.as_view(), name='admin-analytics-overview'),
    path('admin/tracks/<slug:track_slug>/', AdminTrackStatsView.as_view(), name='admin-analytics-track'),
]
