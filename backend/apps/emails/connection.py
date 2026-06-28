"""Build the email connection + from-address from the admin-managed EmailSettings,
falling back to Django's env-configured backend when the panel isn't filled in."""
from django.conf import settings
from django.core.mail import get_connection

from .models import EmailSettings


def build_connection(email_settings=None):
    """Return a Django email connection. Uses the DB SMTP config when a host is
    set; otherwise falls back to settings.EMAIL_BACKEND (console backend in dev)."""
    s = email_settings or EmailSettings.get_solo()
    if s.is_configured():
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=s.host.strip(),
            port=s.port or 587,
            username=(s.username or '').strip(),
            password=s.password or '',
            use_tls=bool(s.use_tls),
            use_ssl=bool(s.use_ssl),
            fail_silently=False,
        )
    return get_connection()  # env-configured backend


def effective_from_email(email_settings=None):
    s = email_settings or EmailSettings.get_solo()
    return (s.from_email or '').strip() or settings.DEFAULT_FROM_EMAIL
