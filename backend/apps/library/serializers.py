from django.conf import settings
from rest_framework import serializers

_GDRIVE_DOWNLOAD = 'https://drive.google.com/uc?export=download&id={}'
_GDRIVE_EMBED    = 'https://drive.google.com/file/d/{}/preview'


def _public_url(key):
    if not key:
        return ''
    public_base = getattr(settings, 'MINIO_PUBLIC_URL', settings.AWS_S3_ENDPOINT_URL).rstrip('/')
    return f"{public_base}/{settings.AWS_STORAGE_BUCKET_NAME}/{key}"


def _pdf_download_url(obj):
    if obj.pdf_key:
        return _public_url(obj.pdf_key)
    if obj.gdrive_pdf_id:
        return _GDRIVE_DOWNLOAD.format(obj.gdrive_pdf_id)
    return ''


def _pdf_embed_url(obj):
    """URL suitable for <iframe> embedding."""
    if obj.pdf_key:
        return _public_url(obj.pdf_key)
    if obj.gdrive_pdf_id:
        return _GDRIVE_EMBED.format(obj.gdrive_pdf_id)
    return ''


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
    is_gdrive_pdf = serializers.SerializerMethodField()
    file_size_mb = serializers.FloatField()
    page_count   = serializers.IntegerField()
    tags         = serializers.ListField(child=serializers.CharField())
    created_at   = serializers.DateTimeField()

    def get_id(self, obj):
        return str(obj.id)

    def get_cover_url(self, obj):
        return _public_url(obj.cover_key)

    def get_has_pdf(self, obj):
        return bool(obj.pdf_key or obj.gdrive_pdf_id)

    def get_has_audio(self, obj):
        return bool(obj.audio_key)

    def get_is_gdrive_pdf(self, obj):
        return bool(not obj.pdf_key and obj.gdrive_pdf_id)


class BookDetailSerializer(BookListSerializer):
    pdf_url       = serializers.SerializerMethodField()
    pdf_embed_url = serializers.SerializerMethodField()
    audio_url     = serializers.SerializerMethodField()
    gdrive_pdf_id = serializers.CharField()

    def get_pdf_url(self, obj):
        return _pdf_download_url(obj)

    def get_pdf_embed_url(self, obj):
        return _pdf_embed_url(obj)

    def get_audio_url(self, obj):
        return _public_url(obj.audio_key)
