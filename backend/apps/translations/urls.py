from django.urls import path
from .views import TranslationSettingsView, PublicLanguagesView

urlpatterns = [
    path('settings/', TranslationSettingsView.as_view(), name='translation-settings'),
    path('languages/', PublicLanguagesView.as_view(), name='translation-languages'),
]
