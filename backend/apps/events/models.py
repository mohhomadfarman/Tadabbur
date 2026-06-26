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
