from rest_framework import serializers


class RegistrationSerializer(serializers.Serializer):
    """Validates an incoming event-registration submission."""
    full_name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=40, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError('Please enter your name.')
        return value

    def validate_email(self, value):
        return value.lower().strip()
