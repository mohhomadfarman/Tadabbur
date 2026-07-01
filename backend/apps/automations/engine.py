"""Event -> evaluate -> send email automation engine. Mirrors
`apps.badges.awards.evaluate_awards`'s shape: a safe no-op when the feature
flag is off, and it never raises into the caller (lesson/track completion,
track enrollment)."""
from datetime import datetime, timezone, timedelta

from apps.features.service import feature_enabled
from apps.emails.transactional import send_transactional_email
from .models import EmailWorkflow, WorkflowSend
from .tasks import send_workflow_reminder


def _resolve_content(rule):
    subject = rule.subject or (rule.template.subject if rule.template else '')
    html_body = rule.html_body or (rule.template.html_body if rule.template else '')
    return subject, html_body


def _send_workflow_email(rule, user, track_slug):
    try:
        subject, html_body = _resolve_content(rule)
        send_transactional_email.delay(subject, html_body, user.email)
        WorkflowSend(
            workflow=rule, user=user, track_slug=track_slug,
            status='sent', sent_at=datetime.now(timezone.utc),
        ).save()
    except Exception:
        pass  # never let a notification failure break the caller


def _already_sent(rule, user, track_slug):
    return WorkflowSend.objects(workflow=rule, user=user, track_slug=track_slug, status='sent').first() is not None


def _already_scheduled(rule, user, track_slug):
    return WorkflowSend.objects(workflow=rule, user=user, track_slug=track_slug, status='scheduled').first() is not None


def handle_trigger(user, trigger_event, track_slug=''):
    """Single entrypoint, called from every hook point (lesson_completed /
    track_completed in MarkCompleteView, track_started in EnrollTrackView).
    `delay_hours` alone decides immediate-vs-delayed — the trigger type doesn't
    hardcode a path, so the rule engine stays genuinely generic. Never raises."""
    try:
        if not feature_enabled('email_automation', user):
            return

        for rule in EmailWorkflow.objects(trigger_event=trigger_event, is_active=True):
            if rule.track_slug and rule.track_slug != track_slug:
                continue
            if not rule.is_enabled_for(user):
                continue

            if rule.delay_hours <= 0:
                # One-shot triggers aren't otherwise protected from double-firing
                # (unlike badges' unique index) — dedupe defensively.
                if _already_sent(rule, user, track_slug):
                    continue
                _send_workflow_email(rule, user, track_slug)
            else:
                if _already_scheduled(rule, user, track_slug):
                    continue
                eta = datetime.now(timezone.utc) + timedelta(hours=rule.delay_hours)
                send = WorkflowSend(
                    workflow=rule, user=user, track_slug=track_slug,
                    status='scheduled', scheduled_for=eta,
                ).save()
                send_workflow_reminder.apply_async(
                    args=[str(rule.id), str(user.id), track_slug, str(send.id)], eta=eta,
                )
    except Exception:
        pass
