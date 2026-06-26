from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime, timezone


class EventRegistration(Document):
    """A lead captured from an event registration form (e.g. the live launch)."""
    full_name = StringField(required=True, max_length=120)
    email = EmailField(required=True)
    phone = StringField(max_length=40, default='')
    country = StringField(max_length=100, default='')
    # Which event this registration is for — lets the same model serve future events.
    event = StringField(default='launch', max_length=50)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'event_registrations',
        'indexes': ['email', 'event', ('event', 'email')],
        'ordering': ['-created_at'],
    }

    def __str__(self):
        return f'{self.email} ({self.event})'


class LaunchSettings(Document):
    """Singleton settings for the /launch page, editable from the admin panel."""
    key = StringField(default='launch', unique=True)
    # ISO 8601 with timezone offset, e.g. '2026-07-15T18:30:00+05:30'. Storing the
    # offset preserves the event's wall-clock time so it displays the same to everyone.
    event_at = StringField(default='2026-07-15T18:30:00+05:30')
    headline = StringField(default='Be there when Tadabbur goes live.')
    intro = StringField(default=(
        'Join us for the official launch of Tadabbur — a free, structured, '
        'scholar-verified Islamic learning platform. Register below to get the '
        'live link and event reminders.'
    ))
    updated_at = DateTimeField()

    meta = {'collection': 'launch_settings'}

    @classmethod
    def get_solo(cls):
        obj = cls.objects(key='launch').first()
        if not obj:
            obj = cls(key='launch')
            obj.save()
        return obj
