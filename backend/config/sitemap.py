"""
Dynamic sitemap.xml generated from published curriculum content.

Mirrors the Vue SPA route shape so every indexable page is discoverable:
  /                                       (home)
  /learn                                  (curriculum index)
  /library, /videos                       (top-level sections)
  /learn/<trackSlug>                      (track)
  /learn/<trackSlug>/<subjectSlug>        (subject)
  /lesson/<lessonSlug>                    (lesson)
  /library/<bookSlug>                     (library book)
"""
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.http import require_GET

from apps.curriculum.models import Track, Subject
from apps.lessons.models import Lesson
from apps.library.models import Book


def _w3c(dt):
    """MongoEngine datetimes -> W3C date (YYYY-MM-DD) for <lastmod>."""
    try:
        return dt.strftime('%Y-%m-%d')
    except Exception:
        return None


def _url(loc, lastmod=None, changefreq=None, priority=None):
    parts = [f'    <loc>{escape(loc)}</loc>']
    if lastmod:
        parts.append(f'    <lastmod>{lastmod}</lastmod>')
    if changefreq:
        parts.append(f'    <changefreq>{changefreq}</changefreq>')
    if priority is not None:
        parts.append(f'    <priority>{priority}</priority>')
    body = '\n'.join(parts)
    return f'  <url>\n{body}\n  </url>'


@require_GET
def sitemap_xml(request):
    base = settings.SITE_URL
    urls = [
        _url(f'{base}/',        changefreq='weekly',  priority='1.0'),
        _url(f'{base}/learn',   changefreq='weekly',  priority='0.9'),
        _url(f'{base}/library', changefreq='weekly',  priority='0.8'),
        _url(f'{base}/videos',  changefreq='weekly',  priority='0.7'),
    ]

    # Tracks
    tracks = Track.objects(is_published=True).order_by('order')
    track_slug_by_id = {}
    for t in tracks:
        track_slug_by_id[str(t.id)] = t.slug
        urls.append(_url(
            f'{base}/learn/{t.slug}',
            lastmod=_w3c(t.updated_at), changefreq='weekly', priority='0.8',
        ))

    # Subjects (only those under a published track)
    subject_track_slug = {}
    subjects = Subject.objects(is_published=True).order_by('order')
    for s in subjects:
        t_slug = track_slug_by_id.get(str(s.track.id)) if s.track else None
        if not t_slug:
            continue
        subject_track_slug[str(s.id)] = t_slug
        urls.append(_url(
            f'{base}/learn/{t_slug}/{s.slug}',
            lastmod=_w3c(s.updated_at), changefreq='weekly', priority='0.7',
        ))

    # Lessons (only those under an indexable subject)
    lessons = Lesson.objects(status='published').order_by('order')
    for l in lessons:
        if not (l.subject and str(l.subject.id) in subject_track_slug):
            continue
        urls.append(_url(
            f'{base}/lesson/{l.slug}',
            lastmod=_w3c(l.updated_at), changefreq='monthly', priority='0.6',
        ))

    # Library books (published)
    for b in Book.objects(is_published=True).order_by('order'):
        urls.append(_url(
            f'{base}/library/{b.slug}',
            lastmod=_w3c(b.updated_at), changefreq='monthly', priority='0.6',
        ))

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(urls)
        + '\n</urlset>\n'
    )
    return HttpResponse(xml, content_type='application/xml')
