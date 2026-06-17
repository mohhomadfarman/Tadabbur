import jwt
from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer,
    UserProfileSerializer, TokenRefreshSerializer,
)
from .utils import generate_tokens, decode_refresh_token


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        user = User(
            email=data['email'],
            username=data['username'],
            full_name=data.get('full_name', ''),
        )
        user.set_password(data['password'])
        user.save()

        tokens = generate_tokens(user)
        return Response(
            {'user': UserProfileSerializer(user).data, **tokens},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            user = User.objects.get(email=data['email'].lower())
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(data['password']):
            return Response(
                {'error': 'Invalid email or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                {'error': 'This account has been deactivated.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.last_login = datetime.now(timezone.utc)
        user.save()

        tokens = generate_tokens(user)
        return Response({'user': UserProfileSerializer(user).data, **tokens})


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = decode_refresh_token(serializer.validated_data['refresh'])
            user = User.objects.get(id=payload['user_id'])
            tokens = generate_tokens(user)
            return Response({'access': tokens['access']})
        except jwt.ExpiredSignatureError:
            return Response(
                {'error': 'Refresh token has expired. Please log in again.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return Response(
                {'error': 'Invalid refresh token.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)

    def patch(self, request):
        user = request.user
        if 'full_name' in request.data:
            user.full_name = request.data['full_name']
        if 'profile' in request.data:
            from .models import UserProfile
            profile_data = request.data['profile']
            if not user.profile:
                user.profile = UserProfile()
            for field in ('bio', 'country', 'preferred_language'):
                if field in profile_data:
                    setattr(user.profile, field, profile_data[field])
        user.save()
        return Response(UserProfileSerializer(user).data)
