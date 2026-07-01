from mongoengine import (
    Document, EmbeddedDocument, ReferenceField, StringField, IntField,
    BooleanField, DateTimeField, EmbeddedDocumentListField,
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
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'categories',
        'indexes': ['slug', 'order'],
    }

    def __str__(self):
        return self.title


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
