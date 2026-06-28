from django.urls import path
from .views import (
    LessonDetailView, AdminLessonListView, AdminLessonDetailView,
    AdminLessonTranslateView, AdminLessonTranslationDetailView,
)

urlpatterns = [
    # Admin must come before the generic slug pattern (otherwise 'admin' matches <slug:slug>)
    path('admin/', AdminLessonListView.as_view(), name='admin-lesson-list'),
    path('admin/<slug:slug>/', AdminLessonDetailView.as_view(), name='admin-lesson-detail'),
    path('admin/<slug:slug>/translate/', AdminLessonTranslateView.as_view(), name='admin-lesson-translate'),
    path('admin/<slug:slug>/translations/<str:code>/', AdminLessonTranslationDetailView.as_view(), name='admin-lesson-translation-detail'),

    # Public
    path('<slug:slug>/', LessonDetailView.as_view(), name='lesson-detail'),
]
