from mongoengine import (
    Document, ReferenceField, StringField, BooleanField,
    DateTimeField, IntField, ListField, DateField, DictField,
)
from datetime import datetime, timezone, date
from apps.users.models import User
from apps.lessons.models import Lesson


class QuizAttempt(Document):
    """Records which answer a user selected for a quiz block."""
    user = ReferenceField(User, required=True)
    lesson_slug = StringField(required=True)
    block_order = IntField(required=True)   # index of the quiz block in content_blocks
    question = StringField()
    selected_index = IntField(required=True)
    selected_answer = StringField()
    correct_index = IntField()
    is_correct = BooleanField()
    attempted_at = DateTimeField()

    meta = {
        'collection': 'quiz_attempts',
        'indexes': [
            'lesson_slug',
            'user',
            ('user', 'lesson_slug', 'block_order'),
        ],
    }


class LessonProgress(Document):
    user = ReferenceField(User, required=True)
    lesson = ReferenceField(Lesson, required=True)
    lesson_slug = StringField(required=True)
    subject_slug = StringField(default='')   # denormalized
    track_slug = StringField(default='')     # denormalized for per-track queries
    completed = BooleanField(default=False)
    completed_at = DateTimeField()

    meta = {
        'collection': 'lesson_progress',
        'indexes': [
            {'fields': ['user', 'lesson'], 'unique': True},
            'user',
            'lesson_slug',
            'track_slug',
        ],
    }


class UserProgress(Document):
    """Per-user aggregate: enrolled tracks, streak, last activity."""
    user = ReferenceField(User, required=True, unique=True)
    enrolled_tracks = ListField(StringField())        # list of track slugs
    track_languages = DictField()                     # { track_slug: lang_code } reading preference
    current_streak_days = IntField(default=0)
    longest_streak_days = IntField(default=0)
    last_activity_date = DateField()                  # date-only for streak calculation
    updated_at = DateTimeField()

    meta = {
        'collection': 'user_progress',
        'indexes': ['user'],
    }

    def update_streak(self):
        """Call after any lesson completion to maintain streak counters."""
        today = date.today()
        if self.last_activity_date is None:
            self.current_streak_days = 1
        elif self.last_activity_date == today:
            pass  # already counted today
        elif (today - self.last_activity_date).days == 1:
            self.current_streak_days += 1
        else:
            # Gap of > 1 day — streak resets
            self.current_streak_days = 1

        if self.current_streak_days > self.longest_streak_days:
            self.longest_streak_days = self.current_streak_days

        self.last_activity_date = today
        self.updated_at = datetime.now(timezone.utc)
