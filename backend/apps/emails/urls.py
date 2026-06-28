from django.urls import path
from .views import (
    AdminEmailSettingsView, AdminTestSendView,
    AdminEmailTemplateListView, AdminEmailTemplateDetailView,
    AdminEmailCampaignListView, AdminEmailCampaignDetailView,
    SendCampaignView, TestSendView, AdminSegmentsView, UnsubscribeView,
)

urlpatterns = [
    # Public one-click unsubscribe (embedded in every campaign email)
    path('unsubscribe/', UnsubscribeView.as_view(), name='email-unsubscribe'),

    # Admin — SMTP settings + generic test-send
    path('admin/settings/', AdminEmailSettingsView.as_view(), name='admin-email-settings'),
    path('admin/test-send/', AdminTestSendView.as_view(), name='admin-email-test-send'),

    # Admin — templates
    path('admin/templates/', AdminEmailTemplateListView.as_view(), name='admin-email-template-list'),
    path('admin/templates/<str:template_id>/', AdminEmailTemplateDetailView.as_view(), name='admin-email-template-detail'),

    # Admin — segments
    path('admin/segments/', AdminSegmentsView.as_view(), name='admin-email-segments'),

    # Admin — campaigns
    path('admin/campaigns/', AdminEmailCampaignListView.as_view(), name='admin-email-campaign-list'),
    path('admin/campaigns/<str:campaign_id>/', AdminEmailCampaignDetailView.as_view(), name='admin-email-campaign-detail'),
    path('admin/campaigns/<str:campaign_id>/send/', SendCampaignView.as_view(), name='admin-email-campaign-send'),
    path('admin/campaigns/<str:campaign_id>/test/', TestSendView.as_view(), name='admin-email-campaign-test'),
]
