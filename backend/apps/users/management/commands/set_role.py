from django.core.management.base import BaseCommand, CommandError
from apps.users.models import User

VALID_ROLES = ['learner', 'author', 'scholar', 'admin']


class Command(BaseCommand):
    help = 'Set the role of a MongoDB user by email.'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email address')
        parser.add_argument('role', type=str, choices=VALID_ROLES, help=f'Role: {", ".join(VALID_ROLES)}')

    def handle(self, *args, **options):
        email = options['email'].lower()
        role = options['role']

        user = User.objects(email=email).first()
        if not user:
            raise CommandError(f'No user found with email: {email}')

        old_role = user.role
        user.role = role
        user.save()

        self.stdout.write(
            self.style.SUCCESS(f'Updated {email}: {old_role} → {role}')
        )
