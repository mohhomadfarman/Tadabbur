from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, StringField, IntField,
    BooleanField, DateTimeField, EmbeddedDocumentListField, ListField,
)
from datetime import datetime, timezone

from config.rebuild import RebuildOnChange


class Level(EmbeddedDocument):
    """A level owned by a Category (e.g. Beginner/Intermediate/Advanced) —
    created inline when the category is authored, not its own collection."""
    name = StringField(required=True, max_length=100)
    slug = StringField(required=True, max_length=100)
    order = IntField(default=0)


class Category(RebuildOnChange, Document):
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True, max_length=200)
    order = IntField(default=0)
    levels = EmbeddedDocumentListField(Level)
    icon_url = StringField(default='')
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'categories',
        'indexes': ['slug', 'order'],
    }

    def __str__(self):
        return self.title


class LearnPageSettings(Document):
    """Singleton settings for the public /learn page, editable from the admin panel."""
    key = StringField(default='learn', unique=True)
    banner_image = StringField(default='')
    # Blank falls back to the default i18n title/subtitle on the frontend.
    banner_title = StringField(default='', max_length=200)
    banner_subtitle = StringField(default='', max_length=300)
    # Title text styling — tuned per background image from the admin panel.
    banner_text_color = StringField(default='#ffffff', max_length=20)
    banner_font_size = IntField(default=30)  # px, title size; subtitle scales proportionally
    banner_text_shadow = BooleanField(default=False)
    updated_at = DateTimeField()

    meta = {'collection': 'learn_page_settings'}

    @classmethod
    def get_solo(cls):
        obj = cls.objects(key='learn').first()
        if not obj:
            obj = cls(key='learn')
            obj.save()
        return obj


class Track(RebuildOnChange, Document):
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True, max_length=200)
    description = StringField(max_length=1000, default='')
    thumbnail_url = StringField(default='')
    order = IntField(default=0)
    is_published = BooleanField(default=False)
    # Taxonomy — optional. `level_slug` is scoped to `category.levels` (Level
    # isn't its own Document, so it's referenced by slug, not id).
    category = ReferenceField(Category, null=True)
    level_slug = StringField(default='')
    # Staged rollout — publish to a handful of testers before everyone.
    # 'all'      -> every user, once is_published
    # 'selected' -> only users whose id is in allowed_user_ids (beta / pre-testing)
    audience = StringField(default='all')
    allowed_user_ids = ListField(StringField())
    # SEO — optional overrides; fall back to title/description when empty
    meta_title = StringField(max_length=70, default='')
    meta_description = StringField(max_length=200, default='')
    og_image = StringField(default='')
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'tracks',
        'indexes': ['slug', 'is_published', 'order', 'category'],
    }

    def is_visible_to(self, user):
        """Resolve whether `user` (or anonymous) can see this track."""
        if not self.is_published:
            return False
        if self.audience != 'selected':
            return True
        uid = getattr(user, 'id', None)
        return bool(uid) and str(uid) in (self.allowed_user_ids or [])

    def __str__(self):
        return self.title


class Subject(RebuildOnChange, Document):
    track = ReferenceField(Track, required=True)
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True, max_length=200)
    description = StringField(max_length=1000, default='')
    thumbnail_url = StringField(default='')
    order = IntField(default=0)
    is_published = BooleanField(default=False)
    # SEO — optional overrides; fall back to title/description when empty
    meta_title = StringField(max_length=70, default='')
    meta_description = StringField(max_length=200, default='')
    og_image = StringField(default='')
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'subjects',
        'indexes': ['slug', 'track', 'is_published', 'order'],
    }

    def __str__(self):
        return self.title
