"""Per-recipient email personalization via plain {{tag}} substitution.

Deliberately NOT a template engine (Jinja2/Django templates) — admin-authored
HTML must never be able to execute template logic. This is a flat regex swap
over a known context dict, nothing more."""
import re

from django.utils.html import escape

_TAG_RE = re.compile(r'\{\{\s*([a-zA-Z0-9_]+)\s*\}\}')

# Drives the admin merge-tag palette. 'universal' tags are available on every
# send; the rest are scoped to a template's slug (or 'automation' for
# workflow-triggered emails outside this feature's retrofit).
MERGE_TAG_CATALOGUE = {
    'universal': ['full_name', 'email'],
    'verification': ['verify_url'],
    'password_reset': ['reset_url'],
    'badge_earned': ['badge_name', 'badge_reward'],
    'automation': ['track_title'],
}


def render_merge_tags(text, context):
    """Substitute {{tag}} occurrences in `text` using `context` (dict of plain
    values). A tag not present in `context` is left untouched (a typo'd tag is
    visibly wrong rather than silently deleted). Present values are HTML-escaped
    before substitution, since some (e.g. full_name) are user-controlled."""
    context = context or {}

    def _sub(match):
        key = match.group(1)
        if key not in context:
            return match.group(0)
        value = context[key]
        return escape('' if value is None else str(value))

    return _TAG_RE.sub(_sub, text or '')
