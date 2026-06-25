from django.core.management.base import BaseCommand
from apps.users.models import Role
from apps.common.permissions import SECTIONS

# Built-in roles. `admin` always resolves to every section (and is immutable);
# scholar/author preserve the reach the old IsAuthorOrAdmin gate gave them.
SYSTEM_ROLES = [
    {'name': 'admin',   'label': 'Admin',   'description': 'Full access to every section.',
     'sections': list(SECTIONS)},
    {'name': 'scholar', 'label': 'Scholar', 'description': 'Authors and reviews content; views analytics.',
     'sections': ['curriculum', 'library', 'videos', 'analytics']},
    {'name': 'author',  'label': 'Author',  'description': 'Authors content; views analytics.',
     'sections': ['curriculum', 'library', 'videos', 'analytics']},
    {'name': 'learner', 'label': 'Learner', 'description': 'Default role for registered users. No admin access.',
     'sections': []},
]


class Command(BaseCommand):
    help = 'Create or update the built-in system roles. Idempotent; safe to re-run.'

    def handle(self, *args, **options):
        for spec in SYSTEM_ROLES:
            role = Role.objects(name=spec['name']).first() or Role(name=spec['name'])
            role.label = spec['label']
            role.description = spec['description']
            role.sections = spec['sections']
            role.is_system = True
            role.save()
            self.stdout.write(self.style.SUCCESS(
                f"Seeded role '{spec['name']}' → {', '.join(spec['sections']) or '(no sections)'}"
            ))
        self.stdout.write(self.style.SUCCESS('System roles ready.'))
