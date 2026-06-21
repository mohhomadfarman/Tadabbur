"""Auto-rebuild the prerendered (SSG) frontend when public content changes.

Call `schedule_rebuild()` after a content mutation (publish / edit / delete of a
Track, Subject, Lesson or Book). It triggers GitHub's `workflow_dispatch` for the
Deploy workflow, which rebuilds the static site so the change gets prerendered.
The build fetches live content, so one triggered rebuild captures everything
published up to build time.

Debounced (trailing): a burst of edits resets a short timer and only the final
quiet moment fires one deploy — an authoring session produces one rebuild, not
dozens. No-op when GITHUB_DEPLOY_TOKEN is unset (auto-rebuild simply disabled).

Caveat: the timer is per-process. With multiple gunicorn workers a burst spread
across workers may fire a few deploys, but the workflow's `concurrency: deploy`
group serializes them, so the effect is just a couple of extra (harmless) builds.
"""
import threading

import requests
from django.conf import settings

# Wait this long after the LAST content change before rebuilding.
_DEBOUNCE_SECONDS = 120
_timer = None
_lock = threading.Lock()


def _dispatch():
    token = settings.GITHUB_DEPLOY_TOKEN
    repo = settings.GITHUB_REPO
    if not token or not repo:
        return
    try:
        requests.post(
            f'https://api.github.com/repos/{repo}/actions/workflows/deploy.yml/dispatches',
            headers={
                'Authorization': f'Bearer {token}',
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28',
            },
            json={'ref': 'main'},
            timeout=10,
        )
    except Exception:
        # A failed dispatch must never break content saving — the next change
        # (or a manual deploy) will rebuild.
        pass


def schedule_rebuild():
    """Debounced trigger for a frontend rebuild. Safe to call on every mutation."""
    if not settings.GITHUB_DEPLOY_TOKEN:
        return
    global _timer
    with _lock:
        if _timer is not None:
            _timer.cancel()
        _timer = threading.Timer(_DEBOUNCE_SECONDS, _dispatch)
        _timer.daemon = True
        _timer.start()


class RebuildOnChange:
    """MongoEngine mixin: schedule a (debounced) frontend rebuild whenever the
    document is saved or deleted. Mix in BEFORE Document, e.g.
    `class Book(RebuildOnChange, Document)`. No-op unless GITHUB_DEPLOY_TOKEN is
    set, so dev/CI and draft edits are unaffected beyond a cheap debounced call.
    """

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        schedule_rebuild()
        return result

    def delete(self, *args, **kwargs):
        schedule_rebuild()
        return super().delete(*args, **kwargs)
