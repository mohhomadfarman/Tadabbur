from django.contrib import admin
from django.urls import path, include

from .sitemap import sitemap_xml
from .redirects import resolve_redirect

urlpatterns = [
    # Mounted at /django-admin (not /admin) so the frontend SPA owns /admin/* and
    # deep admin routes survive a page refresh instead of hitting Django's admin.
    path('django-admin/', admin.site.urls),
    path('sitemap.xml', sitemap_xml, name='sitemap'),
    path('api/v1/redirects/resolve/', resolve_redirect, name='resolve-redirect'),
    path('api/v1/auth/', include('apps.users.urls')),
    path('api/v1/curriculum/', include('apps.curriculum.urls')),
    path('api/v1/lessons/', include('apps.lessons.urls')),
    path('api/v1/progress/', include('apps.progress.urls')),
    path('api/v1/media/',   include('apps.media.urls')),
    path('api/v1/library/', include('apps.library.urls')),
    path('api/v1/videos/',  include('apps.videos.urls')),
    path('api/v1/events/',  include('apps.events.urls')),
    path('api/v1/translations/', include('apps.translations.urls')),
    path('api/v1/announcements/', include('apps.announcements.urls')),
    path('api/v1/features/', include('apps.features.urls')),
    path('api/v1/feedback/', include('apps.feedback.urls')),
    path('api/v1/badges/',   include('apps.badges.urls')),
    path('api/v1/emails/',   include('apps.emails.urls')),
]
