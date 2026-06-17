from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/curriculum/', include('apps.curriculum.urls')),
    path('api/v1/lessons/', include('apps.lessons.urls')),
    path('api/v1/progress/', include('apps.progress.urls')),
    path('api/v1/media/', include('apps.media.urls')),
]
