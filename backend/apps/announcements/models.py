from datetime import datetime, timezone

from mongoengine import (
    Document, ReferenceField, StringField, BooleanField,
    IntField, DateTimeField, EmbeddedDocumentListField,
)

from apps.users.models import User
from apps.lessons.models import ContentBlock  # reuse the lesson block schema


class Announcement(Document):
    """An admin-authored pop-up modal shown to logged-in users."""
    title = StringField(required=True, max_length=200)
    content_blocks = EmbeddedDocumentListField(ContentBlock)
    is_active = BooleanField(default=False)
    # Optional schedule window (UTC). Empty = no bound on that side.
    starts_at = DateTimeField()
    ends_at = DateTimeField()
    priority = IntField(default=0)  # higher shows first
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'announcements',
        'indexes': ['is_active', '-priority', '-created_at'],
    }

    def is_live(self, now=None):
        """Active and within the (optional) schedule window."""
        if not self.is_active:
            return False
        now = now or datetime.now(timezone.utc)
        if self.starts_at and now < _aware(self.starts_at):
            return False
        if self.ends_at and now > _aware(self.ends_at):
            return False
        return True

    def __str__(self):
        return self.title


class AnnouncementView(Document):
    """One row per (user, announcement) — its existence means the user has seen it."""
    user = ReferenceField(User, required=True)
    announcement = ReferenceField(Announcement, required=True, reverse_delete_rule=2)  # CASCADE
    viewed_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    dismissed = BooleanField(default=False)
    dismissed_at = DateTimeField()

    meta = {
        'collection': 'announcement_views',
        'indexes': [
            {'fields': ['user', 'announcement'], 'unique': True},
            'announcement',
        ],
    }


def _aware(dt):
    """MongoEngine may return naive datetimes; treat them as UTC for comparison."""
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
