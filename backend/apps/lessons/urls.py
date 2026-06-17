from django.urls import path
from .views import LessonDetailView, AdminLessonListView, AdminLessonDetailView

urlpatterns = [
    # Public
    path('<slug:slug>/', LessonDetailView.as_view(), name='lesson-detail'),

    # Admin (author+ only) — /api/v1/lessons/admin/ and /api/v1/lessons/admin/<slug>/
    path('admin/', AdminLessonListView.as_view(), name='admin-lesson-list'),
    path('admin/<slug:slug>/', AdminLessonDetailView.as_view(), name='admin-lesson-detail'),
]
