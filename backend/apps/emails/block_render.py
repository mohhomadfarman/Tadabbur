"""Drag-and-drop email block validation + rendering to email-client-safe HTML.
Mirrors apps.lessons.views._normalize_blocks, but with email's own type
vocabulary (layout blocks, not lesson content blocks) and its own renderer,
since email HTML must avoid flexbox/grid and inline every style."""
from django.utils.html import escape

EMAIL_BLOCK_TYPES = ('text', 'header', 'image', 'button', 'divider', 'spacer')

_WRAPPER_OPEN = (
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
    'style="max-width:600px;margin:0 auto;font-family:system-ui,sans-serif">'
)
_WRAPPER_CLOSE = '</table>'


def normalize_email_blocks(raw_list):
    """Validate incoming email blocks; returns (list_of_dicts, error_message)."""
    blocks = []
    for i, raw in enumerate(raw_list or []):
        block_type = (raw.get('type') or '')
        if block_type not in EMAIL_BLOCK_TYPES:
            return None, f'Invalid block type "{block_type}" at index {i}.'
        blocks.append({'type': block_type, 'order': i, 'body': raw.get('body', {}) or {}})
    return blocks, None


def render_blocks_to_html(blocks):
    """Pure function: ordered list of {type, order, body} dicts -> one email-safe
    HTML string. Each block emits its own inline style="" — no <style> tag, no
    flexbox/grid (stripped by Outlook/Gmail), table-based wrapper for consistent
    rendering across clients."""
    rows = []
    for block in sorted(blocks or [], key=lambda b: b.get('order', 0)):
        renderer = _RENDERERS.get(block.get('type'))
        if not renderer:
            continue
        rows.append(f'<tr><td style="padding:0">{renderer(block.get("body") or {})}</td></tr>')
    if not rows:
        return ''
    return _WRAPPER_OPEN + ''.join(rows) + _WRAPPER_CLOSE


def _render_text(body):
    text = escape(body.get('text', ''))
    return f'<p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#222">{text}</p>'


def _render_header(body):
    level = body.get('level') if body.get('level') in ('h1', 'h2') else 'h2'
    text = escape(body.get('text', ''))
    size = '24px' if level == 'h1' else '19px'
    return f'<{level} style="margin:0 0 16px;font-size:{size};line-height:1.3;color:#111">{text}</{level}>'


def _render_image(body):
    url = escape(body.get('url', ''))
    alt = escape(body.get('alt', ''))
    if not url:
        return ''
    img = f'<img src="{url}" alt="{alt}" style="max-width:100%;display:block;border:0;margin:0 0 16px" />'
    link = escape(body.get('link', ''))
    if link:
        return f'<a href="{link}" style="text-decoration:none">{img}</a>'
    return img


def _render_button(body):
    url = escape(body.get('url', ''))
    label = escape(body.get('label', ''))
    if not url or not label:
        return ''
    return (
        f'<p style="text-align:center;margin:28px 0">'
        f'<a href="{url}" style="background:#234ecc;color:#fff;text-decoration:none;'
        f'padding:12px 28px;border-radius:8px;font-weight:600;display:inline-block">{label}</a></p>'
    )


def _render_divider(body):
    return '<hr style="border:none;border-top:1px solid #e5e5e5;margin:24px 0" />'


def _render_spacer(body):
    try:
        height = max(0, min(200, int(body.get('height', 24))))
    except (TypeError, ValueError):
        height = 24
    return f'<div style="height:{height}px;line-height:{height}px">&nbsp;</div>'


_RENDERERS = {
    'text': _render_text,
    'header': _render_header,
    'image': _render_image,
    'button': _render_button,
    'divider': _render_divider,
    'spacer': _render_spacer,
}
