from django.urls import path
from .views import MarkCompleteView, UserProgressView, EnrollTrackView, TrackProgressView

urlpatterns = [
    path('', UserProgressView.as_view(), name='user-progress'),
    path('complete/<slug:slug>/', MarkCompleteView.as_view(), name='mark-complete'),
    path('enroll/<slug:track_slug>/', EnrollTrackView.as_view(), name='enroll-track'),
    path('track/<slug:track_slug>/', TrackProgressView.as_view(), name='track-progress'),
]
