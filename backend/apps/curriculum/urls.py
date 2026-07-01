from django.urls import path
from .views import (
    TrackListView, TrackDetailView, SubjectDetailView,
    AdminTrackListView, AdminTrackDetailView,
    AdminSubjectListView, AdminSubjectDetailView,
    AdminCategoryListView, AdminCategoryDetailView,
)

urlpatterns = [
    # Public
    path('tracks/', TrackListView.as_view(), name='track-list'),
    path('tracks/<slug:slug>/', TrackDetailView.as_view(), name='track-detail'),
    path('subjects/<slug:slug>/', SubjectDetailView.as_view(), name='subject-detail'),

    # Admin (author+ only)
    path('admin/tracks/', AdminTrackListView.as_view(), name='admin-track-list'),
    path('admin/tracks/<slug:slug>/', AdminTrackDetailView.as_view(), name='admin-track-detail'),
    path('admin/subjects/', AdminSubjectListView.as_view(), name='admin-subject-list'),
    path('admin/subjects/<slug:slug>/', AdminSubjectDetailView.as_view(), name='admin-subject-detail'),
    path('admin/categories/', AdminCategoryListView.as_view(), name='admin-category-list'),
    path('admin/categories/<slug:slug>/', AdminCategoryDetailView.as_view(), name='admin-category-detail'),
]
