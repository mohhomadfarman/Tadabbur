from mongoengine import (
    Document, StringField, EmailField, DateTimeField,
    BooleanField, EmbeddedDocument, EmbeddedDocumentField
)
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from datetime import datetime, timezone


class UserProfile(EmbeddedDocument):
    bio = StringField(max_length=500)
    country = StringField(max_length=100)
    preferred_language = StringField(default='en')
    avatar_url = StringField()


class User(Document):
    email = EmailField(required=True, unique=True)
    username = StringField(required=True, unique=True, max_length=50)
    password_hash = StringField(required=True)
    full_name = StringField(max_length=100, default='')
    role = StringField(
        choices=['learner', 'author', 'scholar', 'admin'],
        default='learner'
    )
    profile = EmbeddedDocumentField(UserProfile)
    is_active = BooleanField(default=True)
    is_verified = BooleanField(default=False)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))
    last_login = DateTimeField()

    meta = {
        'collection': 'users',
        'indexes': ['email', 'username']
    }

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password_hash)

    # DRF request.user compatibility
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.email
