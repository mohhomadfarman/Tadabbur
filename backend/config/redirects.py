"""Slug-rename redirect tracking, so a renamed Track/Subject/Lesson/Book URL
301-redirects to its new address instead of soft-404ing (nginx's SPA-shell
fallback otherwise returns HTTP 200 for any unrecognized path — see
frontend/nginx.frontend.conf's `@redirect_check` location, which calls
`resolve_redirect` below before giving up and serving the SPA shell).
"""
from datetime import datetime, timezone

from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.views.decorators.http import require_GET
from mongoengine import Document, StringField, DateTimeField


class SlugRedirect(Document):
    old_path = StringField(required=True, unique=True)
    new_path = StringField(required=True)
    created_at = DateTimeField(default=lambda: datetime.now(timezone.utc))

    meta = {'collection': 'slug_redirects', 'indexes': ['old_path']}


def record_slug_redirect(old_path, new_path):
    """Record that `old_path` now permanently redirects to `new_path`.
    Collapses chains (A->B->C becomes A->C) and clears stale entries so
    `new_path` never appears as a redirect source once it's live again."""
    if old_path == new_path:
        return
    SlugRedirect.objects(new_path=old_path).update(set__new_path=new_path)
    SlugRedirect.objects(old_path=new_path).delete()
    existing = SlugRedirect.objects(old_path=old_path).first()
    if existing:
        existing.new_path = new_path
        existing.save()
    else:
        SlugRedirect(old_path=old_path, new_path=new_path).save()


@require_GET
def resolve_redirect(request):
    """Called by nginx (frontend/nginx.frontend.conf's `@redirect_check`) for
    any request that didn't match a prerendered file. 301s to the new path if
    the requested one was renamed; otherwise 404 so nginx falls back to the
    normal SPA shell."""
    path = request.GET.get('path', '')
    redirect = SlugRedirect.objects(old_path=path).first() if path else None
    if not redirect:
        return HttpResponse(status=404)
    return HttpResponsePermanentRedirect(redirect.new_path)
