from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)
    full_name = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects(email=value.lower()).first():
            raise serializers.ValidationError('An account with this email already exists.')
        return value.lower()

    def validate_username(self, value):
        if User.objects(username=value).first():
            raise serializers.ValidationError('This username is already taken.')
        if not value.replace('_', '').replace('-', '').isalnum():
            raise serializers.ValidationError('Username may only contain letters, numbers, hyphens, and underscores.')
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    email = serializers.EmailField(read_only=True)
    username = serializers.CharField(read_only=True)
    full_name = serializers.CharField()
    role = serializers.CharField(read_only=True)
    sections = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    def get_id(self, obj):
        return str(obj.id)

    def get_sections(self, obj):
        return obj.get_sections()


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
