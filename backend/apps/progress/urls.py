from django.urls import path
from .views import (
    MarkCompleteView, UserProgressView, EnrollTrackView,
    TrackProgressView, SaveQuizAnswerView, AdminLessonStatsView,
    SetTrackLanguageView, TracksProgressView,
)

urlpatterns = [
    path('', UserProgressView.as_view(), name='user-progress'),
    path('complete/<slug:slug>/', MarkCompleteView.as_view(), name='mark-complete'),
    path('quiz/<slug:slug>/', SaveQuizAnswerView.as_view(), name='save-quiz'),
    path('enroll/<slug:track_slug>/', EnrollTrackView.as_view(), name='enroll-track'),
    path('track-language/<slug:track_slug>/', SetTrackLanguageView.as_view(), name='set-track-language'),
    path('tracks-progress/', TracksProgressView.as_view(), name='tracks-progress'),
    path('track/<slug:track_slug>/', TrackProgressView.as_view(), name='track-progress'),
    path('admin/lesson-stats/', AdminLessonStatsView.as_view(), name='admin-lesson-stats'),
]
