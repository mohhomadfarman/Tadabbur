"""System-owned transactional email (verification, password reset, badge-earned).
Fires through the same admin-configured SMTP connection as campaigns
(`deliver_message`), but async via Celery so request handlers never block on
SMTP. Unlike campaigns these are not logged/tracked — just best-effort sends."""
from celery import shared_task


@shared_task(ignore_result=True)
def send_transactional_email(subject, html_body, to_email):
    from .tasks import deliver_message
    deliver_message(subject, html_body, to_email)


def _button(url, label):
    return (
        f'<p style="text-align:center;margin:28px 0">'
        f'<a href="{url}" style="background:#234ecc;color:#fff;text-decoration:none;'
        f'padding:12px 28px;border-radius:8px;font-weight:600;display:inline-block">{label}</a></p>'
    )


def verification_email_body(url):
    return (
        '<p>Assalamu alaikum,</p>'
        '<p>Please confirm your email address to finish setting up your Tadabbur account.</p>'
        f'{_button(url, "Verify email")}'
        '<p style="font-size:13px;color:#888">This link expires in 24 hours. '
        'If you didn\'t create this account, you can ignore this email.</p>'
    )


def password_reset_email_body(url):
    return (
        '<p>Assalamu alaikum,</p>'
        '<p>We received a request to reset your Tadabbur password.</p>'
        f'{_button(url, "Reset password")}'
        '<p style="font-size:13px;color:#888">This link expires in 30 minutes. '
        'If you didn\'t request this, you can safely ignore this email.</p>'
    )


def badge_earned_email_body(badge):
    reward = f'<p>{badge.reward}</p>' if badge.reward else ''
    return (
        f'<p>Assalamu alaikum,</p>'
        f'<p>You just earned the <strong>{badge.name}</strong> badge on Tadabbur!</p>'
        f'{reward}'
        f'<p style="font-size:13px;color:#888">Log in to see it on your dashboard.</p>'
    )
