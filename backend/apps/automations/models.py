from datetime import datetime, timezone

from mongoengine import (
    Document, ReferenceField, StringField, IntField,
    BooleanField, ListField, DateTimeField,
)

from apps.users.models import User
from apps.emails.models import EmailTemplate

TRIGGER_EVENTS = ('track_started', 'track_completed', 'lesson_completed')
SEND_STATUSES = ('scheduled', 'sent', 'skipped', 'failed')


class EmailWorkflow(Document):
    """Admin-defined rule: on `trigger_event` (optionally scoped to one track),
    wait `delay_hours`, optionally re-check the condition still holds, then send
    an email. Separate from EmailCampaign — this is per-user, per-event,
    transactional, not a segment-based marketing blast."""
    name = StringField(required=True, max_length=160)
    trigger_event = StringField(required=True, choices=TRIGGER_EVENTS)
    track_slug = StringField(default='')  # '' = any track (lesson_completed only)
    delay_hours = IntField(default=0)     # 0 = fire immediately; >0 = delayed re-check-and-send
    recheck_condition = BooleanField(default=True)
    template = ReferenceField(EmailTemplate)  # optional, seed-only
    subject = StringField(default='', max_length=300)
    html_body = StringField(default='')
    is_active = BooleanField(default=True)
    # 'all'      → every user the trigger fires for
    # 'selected' → only users whose id is in allowed_user_ids (beta / testing)
    audience = StringField(default='all')
    allowed_user_ids = ListField(StringField())
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'email_workflows',
        'indexes': ['trigger_event', 'is_active', 'track_slug'],
    }

    def is_enabled_for(self, user):
        if not self.is_active:
            return False
        if self.audience != 'selected':
            return True
        uid = getattr(user, 'id', None)
        return bool(uid) and str(uid) in (self.allowed_user_ids or [])

    def __str__(self):
        return self.name


class WorkflowSend(Document):
    """One row per (workflow, user, trigger instance) — makes delayed sends
    resumable/idempotent (the Celery task re-fetches by id) and gives an audit
    trail of what was sent/skipped/failed and why."""
    workflow = ReferenceField(EmailWorkflow, required=True, reverse_delete_rule=2)  # CASCADE
    user = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    track_slug = StringField(default='')
    status = StringField(default='sent', choices=SEND_STATUSES)
    scheduled_for = DateTimeField()
    sent_at = DateTimeField()
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'email_workflow_sends',
        'indexes': [
            'workflow',
            'user',
            ('workflow', 'user', 'track_slug', '-created_at'),
        ],
    }
