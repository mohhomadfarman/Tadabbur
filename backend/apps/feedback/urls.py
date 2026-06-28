from django.urls import path
from .views import SubmitFeedbackView, MyTrackFeedbackView, AdminFeedbackListView

urlpatterns = [
    # Admin must come before the generic <track_slug> patterns
    path('admin/', AdminFeedbackListView.as_view(), name='admin-feedback-list'),

    # Learner-facing
    path('track/<str:track_slug>/', SubmitFeedbackView.as_view(), name='feedback-submit'),
    path('track/<str:track_slug>/me/', MyTrackFeedbackView.as_view(), name='feedback-mine'),
]
