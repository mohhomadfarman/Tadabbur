from django.urls import path
from .views import (
    MarkCompleteView, UserProgressView, EnrollTrackView,
    TrackProgressView, SaveQuizAnswerView, AdminLessonStatsView,
)

urlpatterns = [
    path('', UserProgressView.as_view(), name='user-progress'),
    path('complete/<slug:slug>/', MarkCompleteView.as_view(), name='mark-complete'),
    path('quiz/<slug:slug>/', SaveQuizAnswerView.as_view(), name='save-quiz'),
    path('enroll/<slug:track_slug>/', EnrollTrackView.as_view(), name='enroll-track'),
    path('track/<slug:track_slug>/', TrackProgressView.as_view(), name='track-progress'),
    path('admin/lesson-stats/', AdminLessonStatsView.as_view(), name='admin-lesson-stats'),
]
