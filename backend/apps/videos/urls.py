from django.urls import path

from .views import VideoDetailView, VideoListView

urlpatterns = [
    path('',                VideoListView.as_view(),   name='video-list'),
    path('<str:video_id>/', VideoDetailView.as_view(), name='video-detail'),
]
