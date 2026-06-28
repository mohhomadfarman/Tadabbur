from datetime import datetime, timezone

from mongoengine import (
    Document, ReferenceField, StringField, IntField, DateTimeField,
)

from apps.users.models import User


class TrackFeedback(Document):
    """One rating + optional comment per (user, track). Submitted from the prompt
    shown after a learner completes a whole track."""
    user = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    track_slug = StringField(required=True)
    rating = IntField(required=True, min_value=1, max_value=5)
    comment = StringField(default='', max_length=2000)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'track_feedback',
        'indexes': [
            {'fields': ['user', 'track_slug'], 'unique': True},
            'track_slug',
        ],
    }
