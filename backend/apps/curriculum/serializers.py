from rest_framework import serializers
from .models import Track, Subject


def _track_language_codes(track):
    """Distinct translation language codes present in a track's published lessons.

    Uses an aggregation that returns only the dict keys, so the (potentially
    large) translation payloads are never pulled into memory.
    """
    from apps.lessons.models import Lesson
    subject_ids = list(Subject.objects(track=track, is_published=True).scalar('id'))
    if not subject_ids:
        return set()
    pipeline = [
        {'$match': {'subject': {'$in': subject_ids}, 'status': 'published',
                    'translations': {'$exists': True, '$ne': {}}}},
        {'$project': {'langs': {'$map': {
            'input': {'$objectToArray': '$translations'}, 'as': 'kv', 'in': '$$kv.k'}}}},
        {'$unwind': '$langs'},
        {'$group': {'_id': None, 'codes': {'$addToSet': '$langs'}}},
    ]
    res = list(Lesson.objects.aggregate(pipeline))
    return set(res[0]['codes']) if res else set()


def track_languages(track):
    """Enabled offered languages a track has translations for (with display info)."""
    codes = _track_language_codes(track)
    if not codes:
        return []
    from apps.translations.models import TranslationSettings
    return [
        {'code': l.code, 'name': l.name, 'native_name': l.native_name or '', 'rtl': bool(l.rtl)}
        for l in TranslationSettings.get_solo().enabled_languages() if l.code in codes
    ]


class TrackSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.CharField()
    order = serializers.IntegerField()
    is_published = serializers.SerializerMethodField()
    languages = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_is_published(self, obj):
        return obj.is_published

    def get_languages(self, obj):
        # Skip the extra aggregation for admin list/CRUD responses.
        if self.context.get('admin'):
            return []
        return track_languages(obj)


class SubjectListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.CharField()
    order = serializers.IntegerField()
    is_published = serializers.SerializerMethodField()
    track_slug = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_is_published(self, obj):
        return obj.is_published

    def get_track_slug(self, obj):
        return obj.track.slug if obj.track else ''


class TrackDetailSerializer(TrackSerializer):
    subjects = serializers.SerializerMethodField()
    meta_title = serializers.CharField(default='')
    meta_description = serializers.CharField(default='')
    og_image = serializers.CharField(default='')

    def get_subjects(self, obj):
        subjects = Subject.objects(track=obj, is_published=True).order_by('order')
        return SubjectListSerializer(subjects, many=True).data


class SubjectDetailSerializer(SubjectListSerializer):
    track_id = serializers.SerializerMethodField()
    track_title = serializers.SerializerMethodField()
    track_slug = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    meta_title = serializers.CharField(default='')
    meta_description = serializers.CharField(default='')
    og_image = serializers.CharField(default='')

    def get_track_id(self, obj):
        return str(obj.track.id)

    def get_track_title(self, obj):
        return obj.track.title

    def get_track_slug(self, obj):
        return obj.track.slug

    def get_lessons(self, obj):
        from apps.lessons.serializers import LessonListSerializer
        from apps.lessons.models import Lesson
        lessons = Lesson.objects(subject=obj, status='published').order_by('order')
        return LessonListSerializer(lessons, many=True).data
