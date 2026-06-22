from django.conf import settings
from rest_framework import serializers


def _public_url(key):
    """Return a direct public URL for a MinIO object key.

    Works because tadabbur-media has a public-read bucket policy.
    Simpler and more reliable than presigned URLs — no signatures, no expiry.
    """
    if not key:
        return ''
    public_base = getattr(settings, 'MINIO_PUBLIC_URL', settings.AWS_S3_ENDPOINT_URL).rstrip('/')
    return f"{public_base}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"


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
        return _public_url(obj.cover_key)

    def get_has_pdf(self, obj):
        return bool(obj.pdf_key)

    def get_has_audio(self, obj):
        return bool(obj.audio_key)


class BookDetailSerializer(BookListSerializer):
    pdf_url   = serializers.SerializerMethodField()
    audio_url = serializers.SerializerMethodField()

    def get_pdf_url(self, obj):
        return _public_url(obj.pdf_key)

    def get_audio_url(self, obj):
        return _public_url(obj.audio_key)
