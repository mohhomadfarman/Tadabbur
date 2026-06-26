from datetime import datetime, timezone

from mongoengine.errors import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from .models import EventRegistration
from .serializers import RegistrationSerializer

EVENT = 'launch'


def _iso(dt):
    return dt.isoformat() if dt else None


def _row(r):
    return {
        'id': str(r.id),
        'full_name': r.full_name,
        'email': r.email,
        'phone': r.phone or '',
        'country': r.country or '',
        'created_at': _iso(r.created_at),
    }


class RegisterView(APIView):
    """Public: capture a registration for the live launch."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        data = serializer.validated_data

        # Idempotent by email: a repeat signup is a friendly no-op, not an error.
        if EventRegistration.objects(event=EVENT, email=data['email']).first():
            return Response(
                {'detail': "You're already registered — see you at the launch!", 'already_registered': True},
                status=status.HTTP_200_OK,
            )

        EventRegistration(
            full_name=data['full_name'],
            email=data['email'],
            phone=data.get('phone', '') or '',
            country=data.get('country', '') or '',
            event=EVENT,
        ).save()
        return Response({'detail': "You're registered! We'll be in touch with the details."},
                        status=status.HTTP_201_CREATED)


class AdminRegistrationListView(APIView):
    permission_classes = [section_required('registrations')]

    def get(self, request):
        qs = EventRegistration.objects(event=EVENT).order_by('-created_at')
        return Response([_row(r) for r in qs])


class AdminRegistrationDetailView(APIView):
    permission_classes = [section_required('registrations')]

    def delete(self, request, reg_id):
        try:
            reg = EventRegistration.objects(id=reg_id).first()
        except (ValidationError, Exception):
            reg = None
        if not reg:
            return Response({'detail': 'Registration not found.'}, status=status.HTTP_404_NOT_FOUND)
        reg.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
