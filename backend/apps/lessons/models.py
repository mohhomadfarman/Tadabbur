from mongoengine import (
    Document, EmbeddedDocument, ReferenceField,
    StringField, IntField, DateTimeField,
    EmbeddedDocumentListField, DictField,
)
from datetime import datetime, timezone
from apps.curriculum.models import Subject


class ContentBlock(EmbeddedDocument):
    type = StringField(required=True, choices=['text', 'verse', 'hadith', 'image', 'video', 'quiz'])
    order = IntField(default=0)
    body = DictField()  # flexible payload — schema varies per type

    meta = {'allow_inheritance': False}


class Lesson(Document):
    subject = ReferenceField(Subject, required=True)
    title = StringField(required=True, max_length=300)
    slug = StringField(required=True, unique=True, max_length=300)
    summary = StringField(max_length=500, default='')
    order = IntField(default=0)
    status = StringField(choices=['draft', 'published'], default='draft')
    estimated_minutes = IntField(default=0)
    content_blocks = EmbeddedDocumentListField(ContentBlock)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'lessons',
        'indexes': ['slug', 'subject', 'status', 'order'],
    }

    def __str__(self):
        return self.title
