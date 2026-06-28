"""Recipient-segment resolution + unsubscribe-token signing for email campaigns."""
from django.core import signing
from django.conf import settings

from apps.users.models import User, Role
from apps.events.models import EventRegistration
from .models import Unsubscribe

UNSUB_SALT = 'tadabbur.emails.unsubscribe'


def segment_options():
    """The choosable segments for the campaign editor (key + human label + size hint
    is computed lazily elsewhere). Includes one entry per custom/system role."""
    opts = [
        {'key': 'all_users', 'label': 'All active users'},
        {'key': 'verified_users', 'label': 'Verified users'},
        {'key': 'event_registrations', 'label': 'Event registrations (launch leads)'},
    ]
    for r in Role.objects.order_by('name'):
        opts.append({'key': f'role:{r.name}', 'label': f'Role: {r.label or r.name}'})
    return opts


def resolve_segment(segment):
    """Return a de-duplicated, unsubscribe-filtered list of recipient emails."""
    emails = set()
    seg = (segment or '').strip()
    if seg == 'all_users':
        emails = set(User.objects(is_active=True).scalar('email'))
    elif seg == 'verified_users':
        emails = set(User.objects(is_active=True, is_verified=True).scalar('email'))
    elif seg == 'event_registrations':
        emails = set(EventRegistration.objects.distinct('email'))
    elif seg.startswith('role:'):
        role = seg.split(':', 1)[1]
        emails = set(User.objects(is_active=True, role=role).scalar('email'))

    unsub = set(Unsubscribe.objects.distinct('email'))
    return sorted(e for e in emails if e and e not in unsub)


# ── Unsubscribe tokens (signed, so no per-recipient record is needed up front) ──

def make_unsub_token(email):
    return signing.dumps(email, salt=UNSUB_SALT)


def read_unsub_token(token, max_age=None):
    try:
        return signing.loads(token, salt=UNSUB_SALT, max_age=max_age)
    except signing.BadSignature:
        return None


def unsubscribe_url(email):
    base = settings.SITE_URL.rstrip('/')
    return f'{base}/api/v1/emails/unsubscribe/?token={make_unsub_token(email)}'
