from django.urls import path
from .views import (
    EffectiveFlagsView, AdminFeatureFlagListView, AdminFeatureFlagDetailView,
    FeatureUserSearchView,
)

urlpatterns = [
    # Admin: specific paths must come before the generic <key> pattern
    path('admin/', AdminFeatureFlagListView.as_view(), name='admin-feature-list'),
    path('admin/users/', FeatureUserSearchView.as_view(), name='admin-feature-user-search'),
    path('admin/<str:key>/', AdminFeatureFlagDetailView.as_view(), name='admin-feature-detail'),

    # Learner-facing: resolved flag map for the current user
    path('me/', EffectiveFlagsView.as_view(), name='features-me'),
]
