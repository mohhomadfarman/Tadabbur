from datetime import datetime, timezone

from mongoengine import (
    Document, ReferenceField, StringField, EmailField, DateTimeField, DictField,
    IntField, BooleanField,
)

CAMPAIGN_STATUSES = ('draft', 'scheduled', 'sending', 'sent', 'failed')


class EmailSettings(Document):
    """Singleton SMTP configuration, managed from the admin panel (Admin → Email
    Settings). The password is stored server-side only and never returned in full
    by the API (see views._mask). When `host` is empty the sender falls back to
    Django's env-configured EMAIL_BACKEND (console backend in dev)."""
    key = StringField(default='email', unique=True)
    host = StringField(default='')
    port = IntField(default=587)
    username = StringField(default='')
    password = StringField(default='')      # masked in API responses
    use_tls = BooleanField(default=True)
    use_ssl = BooleanField(default=False)
    from_email = StringField(default='')     # e.g. 'Tadabbur <no-reply@thetadabbur.org>'
    updated_at = DateTimeField()

    meta = {'collection': 'email_settings'}

    @classmethod
    def get_solo(cls):
        obj = cls.objects(key='email').first()
        if not obj:
            obj = cls(key='email')
            obj.save()
        return obj

    def is_configured(self):
        return bool((self.host or '').strip())


class EmailTemplate(Document):
    """A reusable email layout (subject + raw HTML body) authored in the admin."""
    name = StringField(required=True, max_length=160)
    subject = StringField(default='', max_length=300)
    html_body = StringField(default='')
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'email_templates', 'indexes': ['-created_at']}

    def __str__(self):
        return self.name


class EmailCampaign(Document):
    """A send to a recipient segment. Subject + html_body are snapshotted on the
    campaign (optionally seeded from a template) so edits to a template don't
    change what already went out."""
    name = StringField(required=True, max_length=160)
    template = ReferenceField(EmailTemplate)  # optional, for record-keeping
    subject = StringField(default='', max_length=300)
    html_body = StringField(default='')
    # 'all_users' | 'verified_users' | 'event_registrations' | 'role:<name>'
    segment = StringField(default='all_users')
    status = StringField(default='draft', choices=CAMPAIGN_STATUSES)
    scheduled_at = DateTimeField()
    sent_at = DateTimeField()
    stats = DictField()  # {sent, failed, total}
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'email_campaigns', 'indexes': ['status', '-created_at']}

    def __str__(self):
        return self.name


class Unsubscribe(Document):
    """An email address that has opted out. Honored at send time (compliance)."""
    email = EmailField(required=True, unique=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'email_unsubscribes', 'indexes': ['email']}

    def __str__(self):
        return self.email
