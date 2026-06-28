from django.urls import path
from .views import (
    MyBadgesView, UnseenBadgesView, MarkBadgeSeenView,
    AdminBadgeListView, AdminBadgeDetailView, AdminGrantBadgeView,
)

urlpatterns = [
    # Admin must come before the generic <badge_id> patterns
    path('admin/', AdminBadgeListView.as_view(), name='admin-badge-list'),
    path('admin/<str:badge_id>/', AdminBadgeDetailView.as_view(), name='admin-badge-detail'),
    path('admin/<str:badge_id>/grant/', AdminGrantBadgeView.as_view(), name='admin-badge-grant'),

    # Learner-facing
    path('me/', MyBadgesView.as_view(), name='badges-me'),
    path('unseen/', UnseenBadgesView.as_view(), name='badges-unseen'),
    path('<str:badge_id>/seen/', MarkBadgeSeenView.as_view(), name='badge-seen'),
]
