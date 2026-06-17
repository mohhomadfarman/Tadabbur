from rest_framework import serializers
from .models import Track, Subject


class TrackSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.CharField()
    order = serializers.IntegerField()
    is_published = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.id)

    def get_is_published(self, obj):
        return obj.is_published


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

    def get_subjects(self, obj):
        subjects = Subject.objects(track=obj, is_published=True).order_by('order')
        return SubjectListSerializer(subjects, many=True).data


class SubjectDetailSerializer(SubjectListSerializer):
    track_id = serializers.SerializerMethodField()
    track_title = serializers.SerializerMethodField()
    track_slug = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

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
