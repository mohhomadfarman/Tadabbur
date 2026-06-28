"""Celery tasks that actually send email. Auto-discovered via app.autodiscover_tasks()."""
from datetime import datetime, timezone

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

from .models import EmailCampaign
from .connection import build_connection, effective_from_email
from .segments import resolve_segment, unsubscribe_url

UNSUB_FOOTER = (
    '<hr style="margin-top:32px;border:none;border-top:1px solid #eee">'
    '<p style="font-size:12px;color:#888;text-align:center;margin-top:12px">'
    'You received this because you have an account or registered with Tadabbur.<br>'
    '<a href="{url}" style="color:#888">Unsubscribe</a></p>'
)


def _send_one(email, subject, html_body, connection, from_email):
    """Send one HTML email (with a plaintext fallback + unsubscribe footer)."""
    html = (html_body or '') + UNSUB_FOOTER.format(url=unsubscribe_url(email))
    text = strip_tags(html_body or '')
    msg = EmailMultiAlternatives(
        subject=subject or '',
        body=text,
        from_email=from_email,
        to=[email],
        connection=connection,
    )
    msg.attach_alternative(html, 'text/html')
    msg.send(fail_silently=False)


def deliver_message(subject, html_body, to_email):
    """Send a single message synchronously through the admin-configured SMTP.
    Raises on failure so the caller can surface the real error (used by the
    test-send endpoint). Builds its own connection + from-address."""
    _send_one(to_email, subject, html_body, build_connection(), effective_from_email())


@shared_task(ignore_result=True)
def send_campaign(campaign_id):
    campaign = EmailCampaign.objects(id=campaign_id).first()
    if not campaign:
        return
    campaign.status = 'sending'
    campaign.save()

    # One SMTP connection (from the admin-managed settings) reused for the batch.
    connection = build_connection()
    from_email = effective_from_email()

    recipients = resolve_segment(campaign.segment)
    sent = 0
    failed = 0
    for email in recipients:
        try:
            _send_one(email, campaign.subject, campaign.html_body, connection, from_email)
            sent += 1
        except Exception:
            failed += 1

    campaign.stats = {'sent': sent, 'failed': failed, 'total': len(recipients)}
    campaign.status = 'failed' if (failed and sent == 0) else 'sent'
    campaign.sent_at = datetime.now(timezone.utc)
    campaign.save()


@shared_task(ignore_result=True)
def send_test(campaign_id, email):
    campaign = EmailCampaign.objects(id=campaign_id).first()
    if not campaign or not email:
        return
    try:
        _send_one(email, f'[TEST] {campaign.subject}', campaign.html_body,
                  build_connection(), effective_from_email())
    except Exception:
        pass
