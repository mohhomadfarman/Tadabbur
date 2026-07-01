import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generate_tokens(user):
    """Generate a short-lived access token and a long-lived refresh token."""
    now = datetime.now(timezone.utc)

    access_payload = {
        'user_id': str(user.id),
        'email': user.email,
        'role': user.role,
        'sections': user.get_sections(),
        'exp': now + timedelta(hours=1),
        'iat': now,
        'type': 'access',
    }
    refresh_payload = {
        'user_id': str(user.id),
        'exp': now + timedelta(days=30),
        'iat': now,
        'type': 'refresh',
    }

    return {
        'access': jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256'),
        'refresh': jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256'),
    }


def decode_refresh_token(token):
    """Decode and validate a refresh token. Raises jwt.InvalidTokenError on failure."""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    if payload.get('type') != 'refresh':
        raise jwt.InvalidTokenError('Not a refresh token.')
    return payload


def generate_action_token(user, action, minutes):
    """A short-lived, single-purpose JWT (email verification, password reset).
    Stateless by design — no DB row to invalidate, so `action` + `exp` are what
    keep a verify-email link from being replayed as a password-reset link."""
    now = datetime.now(timezone.utc)
    payload = {
        'user_id': str(user.id),
        'action': action,
        'exp': now + timedelta(minutes=minutes),
        'iat': now,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_action_token(token, action):
    """Decode and validate an action token. Raises jwt.InvalidTokenError /
    jwt.ExpiredSignatureError on failure."""
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    if payload.get('action') != action:
        raise jwt.InvalidTokenError('Token is not valid for this action.')
    return payload
