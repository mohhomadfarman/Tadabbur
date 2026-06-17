import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User


class MongoJWTAuthentication(BaseAuthentication):
    """
    Custom DRF authentication class that validates JWT tokens against
    MongoEngine User documents. Replaces django-simplejwt which requires
    Django ORM — our users live in MongoDB.
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ', 1)[1].strip()
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired. Please log in again.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid authentication token.')

        if payload.get('type') != 'access':
            raise AuthenticationFailed('Invalid token type.')

        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User account not found.')

        if not user.is_active:
            raise AuthenticationFailed('User account is deactivated.')

        return (user, token)

    def authenticate_header(self, request):
        return 'Bearer realm="api"'
