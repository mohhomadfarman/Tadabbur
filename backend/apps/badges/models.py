from datetime import datetime, timezone

from mongoengine import (
    Document, ReferenceField, StringField, BooleanField, DateTimeField,
)

from apps.users.models import User

# How a badge is earned.
CRITERIA_TYPES = ('track_complete', 'lessons_count', 'streak', 'manual')


class Badge(Document):
    """An admin-defined achievement. `criteria_value` is interpreted per type:
      - track_complete → a track slug
      - lessons_count  → an integer (as string) of completed lessons
      - streak         → an integer (as string) of current-streak days
      - manual         → ignored (granted explicitly by an admin)
    """
    key = StringField(required=True, unique=True)          # slug
    name = StringField(required=True, max_length=120)
    description = StringField(default='', max_length=500)
    icon_url = StringField(default='')
    criteria_type = StringField(default='manual', choices=CRITERIA_TYPES)
    criteria_value = StringField(default='')
    reward = StringField(default='', max_length=500)        # appreciation / reward text
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'badges', 'indexes': ['key', 'is_active']}

    def __str__(self):
        return self.key


class UserBadge(Document):
    """One row per (user, badge) — its existence means the badge was awarded.
    `seen` flips true once the celebration popup has been shown."""
    user = ReferenceField(User, required=True, reverse_delete_rule=2)   # CASCADE
    badge = ReferenceField(Badge, required=True, reverse_delete_rule=2)  # CASCADE
    awarded_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    seen = BooleanField(default=False)

    meta = {
        'collection': 'user_badges',
        'indexes': [
            {'fields': ['user', 'badge'], 'unique': True},
            'badge',
            {'fields': ['user', 'seen']},
        ],
    }
