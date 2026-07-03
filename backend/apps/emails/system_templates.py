"""Single choke point for sending a "system" transactional email (verification,
password reset, badge earned) through an admin-editable EmailTemplate, with a
guaranteed fallback to hardcoded copy if the template is missing, inactive, or
fails to render. Sending must never break a request handler — this function
never raises."""
import logging

from .block_render import render_blocks_to_html
from .personalize import render_merge_tags
from .transactional import send_transactional_email

logger = logging.getLogger(__name__)


def send_system_email(slug, to_email, context, fallback_subject, fallback_html):
    """Look up an active EmailTemplate by `slug`, render its blocks (or raw
    html_body if it predates the block editor) to HTML, substitute {{tags}} from
    `context`, and send. Falls back to `fallback_subject`/`fallback_html`
    (already-final strings, no merge tags) on any failure."""
    try:
        from .models import EmailTemplate

        tpl = EmailTemplate.objects(slug=slug, is_active=True).order_by('-updated_at').first()
        if not tpl:
            raise LookupError(f'no active system template for slug "{slug}"')

        blocks = [{'type': b.type, 'order': b.order, 'body': b.body} for b in tpl.content_blocks]
        html = render_blocks_to_html(blocks) if blocks else tpl.html_body
        if not html or not html.strip():
            raise ValueError(f'template "{slug}" rendered an empty body')

        subject = render_merge_tags(tpl.subject or fallback_subject, context)
        html = render_merge_tags(html, context)
        send_transactional_email.delay(subject, html, to_email)
    except Exception:
        logger.warning('send_system_email: falling back to hardcoded copy for slug=%s', slug, exc_info=True)
        send_transactional_email.delay(fallback_subject, fallback_html, to_email)
