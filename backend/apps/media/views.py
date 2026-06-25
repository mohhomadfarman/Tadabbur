import uuid
import os
import boto3
from botocore.client import Config
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from apps.common.permissions import any_section_required

ALLOWED_TYPES = {
    'image/jpeg', 'image/png', 'image/webp', 'image/gif',
    'audio/mpeg', 'audio/mp4', 'audio/ogg', 'audio/wav',
    'video/mp4', 'video/webm',
    'application/pdf',
}

FOLDER_MAP = {
    'image':     'lessons/images',
    'audio':     'lessons/audio',
    'video':     'lessons/video',
    'avatar':    'users/avatars',
    'thumbnail': 'thumbnails',
    'book_pdf':  'library/pdfs',
    'book_audio':'library/audio',
    'book_cover':'library/covers',
}


class GenerateUploadURLView(APIView):
    """Return a presigned PUT URL so the browser can upload directly to MinIO."""
    permission_classes = [any_section_required(['curriculum', 'library', 'videos'])]

    def post(self, request):
        filename = (request.data.get('filename') or '').strip()
        content_type = (request.data.get('content_type') or '').strip()
        folder_key = request.data.get('folder', 'image')

        if not filename or not content_type:
            return Response(
                {'detail': 'filename and content_type are required.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if content_type not in ALLOWED_TYPES:
            return Response(
                {'detail': f'Content type "{content_type}" is not allowed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        folder = FOLDER_MAP.get(folder_key, 'lessons/images')
        ext = os.path.splitext(filename)[1].lower()
        key = f"{folder}/{uuid.uuid4()}{ext}"

        public_base = getattr(settings, 'MINIO_PUBLIC_URL', settings.AWS_S3_ENDPOINT_URL).rstrip('/')
        s3 = boto3.client(
            's3',
            endpoint_url=public_base,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version='s3v4'),
            verify=settings.AWS_S3_VERIFY,
        )

        presigned_url = s3.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': key,
                'ContentType': content_type,
            },
            ExpiresIn=300,
        )

        public_url = f"{public_base}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"

        return Response({
            'upload_url': presigned_url,
            'public_url': public_url,
            'key': key,
        })
