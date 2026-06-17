from mongoengine import Document, ReferenceField, StringField, IntField, BooleanField, DateTimeField
from datetime import datetime, timezone


class Track(Document):
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True, max_length=200)
    description = StringField(max_length=1000, default='')
    thumbnail_url = StringField(default='')
    order = IntField(default=0)
    is_published = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'tracks',
        'indexes': ['slug', 'is_published', 'order'],
    }

    def __str__(self):
        return self.title


class Subject(Document):
    track = ReferenceField(Track, required=True)
    title = StringField(required=True, max_length=200)
    slug = StringField(required=True, unique=True, max_length=200)
    description = StringField(max_length=1000, default='')
    thumbnail_url = StringField(default='')
    order = IntField(default=0)
    is_published = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'subjects',
        'indexes': ['slug', 'track', 'is_published', 'order'],
    }

    def __str__(self):
        return self.title
