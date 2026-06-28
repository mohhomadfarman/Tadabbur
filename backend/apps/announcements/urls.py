from django.urls import path
from .views import (
    ActiveAnnouncementsView, RecordViewView, DismissView,
    AdminAnnouncementListView, AdminAnnouncementDetailView,
)

urlpatterns = [
    # Admin must come before the generic <id> patterns
    path('admin/', AdminAnnouncementListView.as_view(), name='admin-announcement-list'),
    path('admin/<str:announcement_id>/', AdminAnnouncementDetailView.as_view(), name='admin-announcement-detail'),

    # Learner-facing
    path('active/', ActiveAnnouncementsView.as_view(), name='announcements-active'),
    path('<str:announcement_id>/view/', RecordViewView.as_view(), name='announcement-view'),
    path('<str:announcement_id>/dismiss/', DismissView.as_view(), name='announcement-dismiss'),
]
