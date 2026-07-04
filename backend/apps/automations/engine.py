"""Event -> evaluate -> send email automation engine. Mirrors
`apps.badges.awards.evaluate_awards`'s shape: a safe no-op when the feature
flag is off, and it never raises into the caller (lesson/track completion,
track enrollment)."""
import logging
from datetime import datetime, timezone, timedelta

from apps.features.service import feature_enabled
from apps.emails.transactional import send_transactional_email
from .models import EmailWorkflow, WorkflowSend
from .tasks import send_workflow_reminder

logger = logging.getLogger(__name__)


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
    except Exception as e:
        # Never let a notification failure break the caller — but unlike
        # before, don't let it vanish without a trace either. Separate
        # try/except for the audit write so a broken DB write here can't
        # also get swallowed silently.
        logger.exception('workflow %s send failed for user %s', rule.id, user.id)
        try:
            WorkflowSend(
                workflow=rule, user=user, track_slug=track_slug,
                status='failed', reason=str(e)[:500],
            ).save()
        except Exception:
            pass


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
                # Only reachable for audience='selected' (audience='all' is
                # always enabled) — record it so a rule scoped away from the
                # user testing it doesn't look identical to "nothing happened".
                try:
                    WorkflowSend(
                        workflow=rule, user=user, track_slug=track_slug,
                        status='skipped', reason='audience',
                    ).save()
                except Exception:
                    pass
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
        logger.exception('handle_trigger failed for event=%s track=%s', trigger_event, track_slug)
