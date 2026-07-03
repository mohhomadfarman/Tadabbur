from datetime import datetime, timezone

from django.core.management.base import BaseCommand

from apps.emails.block_render import render_blocks_to_html
from apps.emails.models import EmailBlock, EmailTemplate
from apps.emails.seed_data import SYSTEM_TEMPLATE_SEEDS


class Command(BaseCommand):
    help = (
        'Create the default system EmailTemplate rows (verification, '
        'password_reset, badge_earned) if they do not already exist. Idempotent '
        'and conservative: only creates a row when no template with that slug '
        'exists yet — never overwrites an admin-edited template on re-run.'
    )

    def handle(self, *args, **options):
        now = datetime.now(timezone.utc)
        for spec in SYSTEM_TEMPLATE_SEEDS:
            if EmailTemplate.objects(slug=spec['slug']).first():
                self.stdout.write(f"Skipping '{spec['slug']}' — already exists.")
                continue
            blocks = [EmailBlock(**b) for b in spec['content_blocks']]
            html = render_blocks_to_html(spec['content_blocks'])
            EmailTemplate(
                name=spec['name'],
                slug=spec['slug'],
                subject=spec['subject'],
                content_blocks=blocks,
                html_body=html,
                is_active=True,
                created_at=now,
                updated_at=now,
            ).save()
            self.stdout.write(self.style.SUCCESS(f"Created system template '{spec['slug']}'"))
        self.stdout.write(self.style.SUCCESS('System email templates ready.'))
