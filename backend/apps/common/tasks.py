"""Celery tasks for cross-cutting concerns. Auto-discovered via
app.autodiscover_tasks() (see backend/celery_app.py)."""
import requests
from celery import shared_task
from django.conf import settings


@shared_task(ignore_result=True)
def dispatch_frontend_rebuild():
    """Fire a GitHub Actions workflow_dispatch for deploy.yml, rebuilding the
    prerendered frontend against current content. Scheduled (debounced) from
    config.rebuild.schedule_rebuild() whenever published content changes."""
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
        # A failed dispatch must never break anything — the next content
        # change (or a manual deploy) will rebuild.
        pass
