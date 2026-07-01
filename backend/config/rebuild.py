"""Auto-rebuild the prerendered (SSG) frontend when public content changes.

Mix `RebuildOnChange` into a MongoEngine Document (before `Document`) and every
save/delete schedules a debounced GitHub Actions dispatch of deploy.yml, which
rebuilds the frontend against the current sitemap/content. No-op unless
GITHUB_DEPLOY_TOKEN is set, so dev/CI and draft edits are unaffected beyond a
cheap Redis SET on every mutation.

Debounce lives in Redis (SET NX EX), not in-process `threading.Timer` state —
gunicorn runs multiple worker processes, so per-process timers don't coordinate
across them and this schedules once per window regardless of which worker
handled the save. The actual GitHub dispatch runs in a Celery task
(apps.common.tasks.dispatch_frontend_rebuild), fully decoupled from the web
request/response cycle, so a dispatch failure can never turn into a 500 on a
content save.
"""
import redis
from django.conf import settings

_DEBOUNCE_SECONDS = 120
_LOCK_KEY = 'tadabbur:frontend-rebuild:pending'


def schedule_rebuild():
    """Debounced trigger for a frontend rebuild. Safe to call on every mutation
    — never raises, so it can never break the caller's save()/delete()."""
    if not settings.GITHUB_DEPLOY_TOKEN:
        return
    try:
        client = redis.Redis.from_url(settings.CELERY_BROKER_URL)
        # Only the first save in a debounce window schedules a dispatch; later
        # saves within the window are already covered by it.
        if client.set(_LOCK_KEY, '1', nx=True, ex=_DEBOUNCE_SECONDS):
            from apps.common.tasks import dispatch_frontend_rebuild
            dispatch_frontend_rebuild.apply_async(countdown=_DEBOUNCE_SECONDS)
    except Exception:
        pass


class RebuildOnChange:
    """MongoEngine mixin: schedule a (debounced) frontend rebuild whenever the
    document is saved or deleted. Mix in BEFORE Document, e.g.
    `class Book(RebuildOnChange, Document)`."""

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        schedule_rebuild()
        return result

    def delete(self, *args, **kwargs):
        result = super().delete(*args, **kwargs)
        schedule_rebuild()
        return result
