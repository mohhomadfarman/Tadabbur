from django.core.management.base import BaseCommand

from apps.features.models import FeatureFlag
from apps.features.registry import FEATURE_REGISTRY


class Command(BaseCommand):
    help = (
        'Materialize a FeatureFlag row for every key in the registry. Idempotent; '
        'safe to re-run. Preserves admin-set enabled/audience/allowed_user_ids on '
        'existing rows — only fills metadata + defaults for new keys.'
    )

    def handle(self, *args, **options):
        for spec in FEATURE_REGISTRY:
            flag = FeatureFlag.objects(key=spec['key']).first()
            if flag:
                # Keep admin-set state; refresh denormalized display metadata only.
                flag.label = spec['label']
                flag.description = spec['description']
                flag.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Synced flag '{spec['key']}' (enabled={flag.enabled}, audience={flag.audience})"
                ))
            else:
                flag = FeatureFlag(
                    key=spec['key'],
                    label=spec['label'],
                    description=spec['description'],
                    enabled=bool(spec.get('default_enabled', False)),
                    audience='all',
                )
                flag.save()
                self.stdout.write(self.style.SUCCESS(
                    f"Created flag '{spec['key']}' (default enabled={flag.enabled})"
                ))
        self.stdout.write(self.style.SUCCESS('Feature flags ready.'))
