from django.urls import path
from .views import GenerateUploadURLView

urlpatterns = [
    path('upload-url/', GenerateUploadURLView.as_view(), name='upload-url'),
]
