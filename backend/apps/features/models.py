from datetime import datetime, timezone

from mongoengine import Document, StringField, BooleanField, ListField, DateTimeField

from .registry import get_spec


class FeatureFlag(Document):
    """The admin-editable state of one feature key. The set of valid keys is
    defined in registry.py; one row is materialized per key by seed_feature_flags."""
    key = StringField(required=True, unique=True)
    # Denormalized from the registry for display in the admin list.
    label = StringField(default='')
    description = StringField(default='')
    enabled = BooleanField(default=False)
    # 'all'      → every user (subject to `enabled`)
    # 'selected' → only users whose id is in allowed_user_ids (beta / pre-testing)
    audience = StringField(default='all')
    allowed_user_ids = ListField(StringField())  # ObjectId strings; only used when audience='selected'
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'feature_flags', 'indexes': ['key']}

    @classmethod
    def get_or_create(cls, key):
        """Fetch the row for `key`, creating it from the registry defaults if absent."""
        obj = cls.objects(key=key).first()
        if not obj:
            spec = get_spec(key) or {}
            obj = cls(
                key=key,
                label=spec.get('label', ''),
                description=spec.get('description', ''),
                enabled=bool(spec.get('default_enabled', False)),
                audience='all',
            )
            obj.save()
        return obj

    def is_enabled_for(self, user):
        """Resolve this flag for a specific user (or anonymous)."""
        if not self.enabled:
            return False
        if self.audience != 'selected':
            return True
        # 'selected': requires an authenticated user in the allow-list.
        uid = getattr(user, 'id', None)
        return bool(uid) and str(uid) in (self.allowed_user_ids or [])

    def __str__(self):
        return self.key
