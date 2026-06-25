from mongoengine import (
    Document, StringField, EmailField, DateTimeField,
    BooleanField, EmbeddedDocument, EmbeddedDocumentField, ListField,
)
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from datetime import datetime, timezone

from apps.common.permissions import SECTIONS

# Fallback section grants for the built-in role names, used only when no Role
# document exists yet (e.g. before `seed_roles` runs). Guarantees existing users
# keep the access they had before custom roles were introduced.
_SYSTEM_ROLE_SECTIONS = {
    'admin': list(SECTIONS),
    'scholar': ['curriculum', 'library', 'videos', 'analytics'],
    'author': ['curriculum', 'library', 'videos', 'analytics'],
    'learner': [],
}


class Role(Document):
    """A named set of section grants. `name` is what gets stored on User.role."""
    name = StringField(required=True, unique=True, max_length=50)
    label = StringField(max_length=80, default='')
    description = StringField(max_length=300, default='')
    sections = ListField(StringField())          # subset of SECTIONS
    is_system = BooleanField(default=False)       # built-ins: protected from edit/delete
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'roles', 'indexes': ['name']}

    def __str__(self):
        return self.name


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
    # Stores a Role.name. No fixed `choices` so custom roles are allowed; the
    # name is validated against the roles collection when assigned via the API.
    role = StringField(default='learner', max_length=50)
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

    def get_sections(self):
        """Resolve this user's role to its granted sections. Admin always gets
        every section. Falls back to the built-in defaults when no Role doc
        exists yet, so access never breaks before `seed_roles` runs."""
        role = Role.objects(name=self.role).first()
        if role:
            return list(SECTIONS) if role.name == 'admin' else list(role.sections or [])
        return list(_SYSTEM_ROLE_SECTIONS.get(self.role, []))

    # DRF request.user compatibility
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.email
