from datetime import datetime, timezone
from mongoengine import (
    Document, StringField, BooleanField, IntField,
    FloatField, ListField, DateTimeField,
)

from config.rebuild import RebuildOnChange


class Book(RebuildOnChange, Document):
    title        = StringField(required=True, max_length=300)
    slug         = StringField(required=True, unique=True, max_length=300)
    author       = StringField(max_length=200, default='')
    description  = StringField(max_length=3000, default='')
    category     = StringField(max_length=100, default='')
    language     = StringField(
        choices=['en', 'ar', 'ur', 'fr', 'id', 'other'],
        default='en',
    )
    cover_key    = StringField(default='')   # MinIO object key for cover image
    pdf_key      = StringField(default='')   # MinIO object key for PDF file
    audio_key    = StringField(default='')   # MinIO object key for audiobook (optional)
    gdrive_pdf_id = StringField(default='') # Google Drive file ID (used when pdf_key is absent)
    file_size_mb = FloatField(default=0.0)
    page_count   = IntField(default=0)
    is_published = BooleanField(default=False)
    order        = IntField(default=0)
    tags         = ListField(StringField())
    created_at   = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at   = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'books',
        'indexes': ['slug', 'is_published', 'category', 'language', 'order'],
        'ordering': ['order', 'title'],
    }

    def __str__(self):
        return self.title
