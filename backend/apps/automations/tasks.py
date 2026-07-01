"""Celery task for delayed automation reminders. Auto-discovered via
app.autodiscover_tasks() (see backend/celery_app.py)."""
from datetime import datetime, timezone

from celery import shared_task

from apps.users.models import User
from apps.progress.completion import track_is_complete
from apps.emails.transactional import send_transactional_email
from .models import EmailWorkflow, WorkflowSend


@shared_task(ignore_result=True)
def send_workflow_reminder(rule_id, user_id, track_slug, workflow_send_id):
    """Fires at the rule's `eta`. Re-fetches everything fresh so edits made to
    the rule between scheduling and firing are honored automatically, and
    updates the existing (already-'scheduled') WorkflowSend row rather than
    creating a new one."""
    rule = EmailWorkflow.objects(id=rule_id).first()
    send = WorkflowSend.objects(id=workflow_send_id).first()
    user = User.objects(id=user_id).first()

    if not rule or not send or not user:
        return
    if send.status != 'scheduled':
        return  # already handled (idempotency guard against double-firing)
    if not rule.is_active:
        send.status = 'skipped'
        send.save()
        return

    if rule.recheck_condition and rule.trigger_event == 'track_started':
        # A learner who finished in the meantime shouldn't get a stale
        # "keep going" reminder.
        if track_is_complete(user, track_slug):
            send.status = 'skipped'
            send.save()
            return

    try:
        subject = rule.subject or (rule.template.subject if rule.template else '')
        html_body = rule.html_body or (rule.template.html_body if rule.template else '')
        send_transactional_email.delay(subject, html_body, user.email)
        send.status = 'sent'
        send.sent_at = datetime.now(timezone.utc)
        send.save()
    except Exception:
        try:
            send.status = 'failed'
            send.save()
        except Exception:
            pass
