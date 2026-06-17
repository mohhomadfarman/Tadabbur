import boto3
from botocore.client import Config
from django.conf import settings
from rest_framework import serializers


def _presign(key, expires=3600):
    """Return a presigned GET URL for a MinIO object key, or '' if key is empty."""
    if not key:
        return ''
    s3 = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version='s3v4'),
        verify=False,
    )
    return s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=expires,
    )


class BookListSerializer(serializers.Serializer):
    id           = serializers.SerializerMethodField()
    title        = serializers.CharField()
    slug         = serializers.CharField()
    author       = serializers.CharField()
    description  = serializers.CharField()
    category     = serializers.CharField()
    language     = serializers.CharField()
    cover_url    = serializers.SerializerMethodField()
    has_pdf      = serializers.SerializerMethodField()
    has_audio    = serializers.SerializerMethodField()
    file_size_mb = serializers.FloatField()
    page_count   = serializers.IntegerField()
    tags         = serializers.ListField(child=serializers.CharField())
    created_at   = serializers.DateTimeField()

    def get_id(self, obj):
        return str(obj.id)

    def get_cover_url(self, obj):
        # Cover images can be long-lived (24h)
        return _presign(obj.cover_key, 86400) if obj.cover_key else ''

    def get_has_pdf(self, obj):
        return bool(obj.pdf_key)

    def get_has_audio(self, obj):
        return bool(obj.audio_key)


class BookDetailSerializer(BookListSerializer):
    pdf_url      = serializers.SerializerMethodField()
    audio_url    = serializers.SerializerMethodField()

    def get_pdf_url(self, obj):
        # PDF URLs expire in 2 hours — enough time to read
        return _presign(obj.pdf_key, 7200) if obj.pdf_key else ''

    def get_audio_url(self, obj):
        return _presign(obj.audio_key, 7200) if obj.audio_key else ''
