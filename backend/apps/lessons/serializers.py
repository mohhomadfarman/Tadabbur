import math
from rest_framework import serializers
from .models import Lesson, ContentBlock


class ContentBlockSerializer(serializers.Serializer):
    type = serializers.CharField()
    order = serializers.IntegerField()
    body = serializers.DictField()


class LessonListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    title = serializers.CharField()
    slug = serializers.CharField()
    summary = serializers.CharField()
    order = serializers.IntegerField()
    estimated_minutes = serializers.IntegerField()

    def get_id(self, obj):
        return str(obj.id)


class LessonDetailSerializer(LessonListSerializer):
    subject_id = serializers.SerializerMethodField()
    subject_title = serializers.SerializerMethodField()
    subject_slug = serializers.SerializerMethodField()
    is_truncated = serializers.SerializerMethodField()
    content_blocks = serializers.SerializerMethodField()
    prev_lesson = serializers.SerializerMethodField()
    next_lesson = serializers.SerializerMethodField()

    def get_subject_id(self, obj):
        return str(obj.subject.id)

    def get_subject_title(self, obj):
        return obj.subject.title

    def get_subject_slug(self, obj):
        return obj.subject.slug

    def get_is_truncated(self, obj):
        return self.context.get('truncate', False)

    def get_content_blocks(self, obj):
        blocks = sorted(obj.content_blocks, key=lambda b: b.order)
        if self.context.get('truncate', False):
            visible = max(1, math.ceil(len(blocks) * 0.25))
            blocks = blocks[:visible]
        return ContentBlockSerializer(blocks, many=True).data

    def get_prev_lesson(self, obj):
        prev = Lesson.objects(
            subject=obj.subject, status='published', order__lt=obj.order
        ).order_by('-order').first()
        return {'slug': prev.slug, 'title': prev.title} if prev else None

    def get_next_lesson(self, obj):
        nxt = Lesson.objects(
            subject=obj.subject, status='published', order__gt=obj.order
        ).order_by('order').first()
        return {'slug': nxt.slug, 'title': nxt.title} if nxt else None
