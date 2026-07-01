from mongoengine import (
    Document, EmbeddedDocument, ReferenceField,
    StringField, IntField, DateTimeField, DateField,
    EmbeddedDocumentListField, DictField,
)
from datetime import datetime, timezone
from apps.curriculum.models import Subject
from apps.users.models import User
from config.rebuild import RebuildOnChange


class ContentBlock(EmbeddedDocument):
    type = StringField(required=True, choices=['text', 'verse', 'hadith', 'image', 'video', 'quiz'])
    order = IntField(default=0)
    body = DictField()  # flexible payload — schema varies per type

    meta = {'allow_inheritance': False}


class Lesson(RebuildOnChange, Document):
    subject = ReferenceField(Subject, required=True)
    title = StringField(required=True, max_length=300)
    slug = StringField(required=True, unique=True, max_length=300)
    summary = StringField(max_length=500, default='')
    order = IntField(default=0)
    status = StringField(choices=['draft', 'published'], default='draft')
    estimated_minutes = IntField(default=0)
    content_blocks = EmbeddedDocumentListField(ContentBlock)
    # AI translations keyed by language code, e.g.
    #   { 'hinglish': { title, summary, meta_title, meta_description,
    #                   content_blocks: [...], source_updated_at, model,
    #                   translated_at, edited } }
    # The original (source) language always lives in the top-level fields above.
    translations = DictField()
    # SEO — optional overrides; fall back to title/summary when empty
    meta_title = StringField(max_length=70, default='')
    meta_description = StringField(max_length=200, default='')
    og_image = StringField(default='')
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'lessons',
        'indexes': ['slug', 'subject', 'status', 'order'],
    }

    def __str__(self):
        return self.title


class LessonView(Document):
    """One row per (user, lesson, day) — a dedupe'd 'read' event, so admin
    analytics can answer 'how many users read content today/this week' without
    unbounded write volume from every page load/refresh."""
    user = ReferenceField(User, required=True, reverse_delete_rule=2)  # CASCADE
    lesson_slug = StringField(required=True)
    track_slug = StringField(default='')  # denormalized, like LessonProgress
    view_date = DateField(required=True)  # UTC day — part of the daily-unique index
    viewed_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {
        'collection': 'lesson_views',
        'indexes': [
            {'fields': ['user', 'lesson_slug', 'view_date'], 'unique': True},
            'view_date',
            'track_slug',
        ],
    }
