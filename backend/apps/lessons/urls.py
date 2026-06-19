from django.urls import path
from .views import LessonDetailView, AdminLessonListView, AdminLessonDetailView

urlpatterns = [
    # Admin must come before the generic slug pattern (otherwise 'admin' matches <slug:slug>)
    path('admin/', AdminLessonListView.as_view(), name='admin-lesson-list'),
    path('admin/<slug:slug>/', AdminLessonDetailView.as_view(), name='admin-lesson-detail'),

    # Public
    path('<slug:slug>/', LessonDetailView.as_view(), name='lesson-detail'),
]
