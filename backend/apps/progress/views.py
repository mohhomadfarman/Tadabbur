from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.lessons.models import Lesson
from apps.curriculum.models import Track, Subject
from .models import LessonProgress, UserProgress


def _get_or_create_user_progress(user):
    up = UserProgress.objects(user=user).first()
    if not up:
        up = UserProgress(user=user, enrolled_tracks=[], updated_at=datetime.now(timezone.utc))
        up.save()
    return up


class MarkCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        lesson = Lesson.objects(slug=slug, status='published').first()
        if not lesson:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        subject_slug = lesson.subject.slug
        track_slug = lesson.subject.track.slug if lesson.subject.track else ''

        lp = LessonProgress.objects(user=request.user, lesson=lesson).first()
        if not lp:
            lp = LessonProgress(
                user=request.user,
                lesson=lesson,
                lesson_slug=slug,
                subject_slug=subject_slug,
                track_slug=track_slug,
            )

        already_done = lp.completed
        lp.completed = True
        lp.completed_at = datetime.now(timezone.utc)
        lp.save()

        if not already_done:
            up = _get_or_create_user_progress(request.user)
            up.update_streak()
            up.save()

        return Response({'lesson_slug': slug, 'completed': True})


class UserProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        completed_qs = LessonProgress.objects(user=request.user, completed=True)
        completed_slugs = list(completed_qs.scalar('lesson_slug'))

        up = UserProgress.objects(user=request.user).first()

        enrolled_tracks = []
        current_streak = 0
        longest_streak = 0
        last_activity = None

        if up:
            enrolled_tracks = up.enrolled_tracks or []
            current_streak = up.current_streak_days or 0
            longest_streak = up.longest_streak_days or 0
            last_activity = up.last_activity_date.isoformat() if up.last_activity_date else None

        # Continue learning: last completed lesson, pick its next sibling if available
        continue_learning = None
        last_lp = LessonProgress.objects(
            user=request.user, completed=True
        ).order_by('-completed_at').first()

        if last_lp:
            try:
                last_lesson = last_lp.lesson
                nxt = Lesson.objects(
                    subject=last_lesson.subject,
                    status='published',
                    order__gt=last_lesson.order,
                ).order_by('order').first()
                target = nxt if nxt else last_lesson
                continue_learning = {
                    'lesson_slug': target.slug,
                    'lesson_title': target.title,
                    'subject_title': target.subject.title,
                    'subject_slug': target.subject.slug,
                    'track_slug': last_lp.track_slug,
                }
            except Exception:
                pass

        return Response({
            'completed_lessons': completed_slugs,
            'total_lessons_completed': len(completed_slugs),
            'enrolled_tracks': enrolled_tracks,
            'current_streak_days': current_streak,
            'longest_streak_days': longest_streak,
            'last_activity': last_activity,
            'continue_learning': continue_learning,
        })


class EnrollTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, track_slug):
        track = Track.objects(slug=track_slug, is_published=True).first()
        if not track:
            return Response({'detail': 'Track not found.'}, status=status.HTTP_404_NOT_FOUND)

        up = _get_or_create_user_progress(request.user)
        if track_slug not in up.enrolled_tracks:
            up.enrolled_tracks.append(track_slug)
            up.updated_at = datetime.now(timezone.utc)
            up.save()
            return Response({'enrolled': True, 'track_slug': track_slug})

        return Response({'enrolled': True, 'track_slug': track_slug})

    def delete(self, request, track_slug):
        up = UserProgress.objects(user=request.user).first()
        if up and track_slug in up.enrolled_tracks:
            up.enrolled_tracks.remove(track_slug)
            up.updated_at = datetime.now(timezone.utc)
            up.save()
        return Response({'enrolled': False, 'track_slug': track_slug})


class TrackProgressView(APIView):
    """Completion breakdown for one enrolled track."""
    permission_classes = [IsAuthenticated]

    def get(self, request, track_slug):
        track = Track.objects(slug=track_slug, is_published=True).first()
        if not track:
            return Response({'detail': 'Track not found.'}, status=status.HTTP_404_NOT_FOUND)

        subjects = Subject.objects(track=track, is_published=True).order_by('order')
        completed_in_track = set(
            LessonProgress.objects(
                user=request.user, track_slug=track_slug, completed=True
            ).scalar('lesson_slug')
        )

        total_all = 0
        subjects_data = []

        for subj in subjects:
            lessons = list(Lesson.objects(subject=subj, status='published').scalar('slug'))
            total = len(lessons)
            done = sum(1 for s in lessons if s in completed_in_track)
            total_all += total
            subjects_data.append({
                'subject_slug': subj.slug,
                'subject_title': subj.title,
                'total_lessons': total,
                'completed_lessons': done,
                'percent': round(done / total * 100) if total else 0,
            })

        completed_all = len(completed_in_track)
        return Response({
            'track_slug': track_slug,
            'track_title': track.title,
            'total_lessons': total_all,
            'completed_lessons': completed_all,
            'percent': round(completed_all / total_all * 100) if total_all else 0,
            'subjects': subjects_data,
        })
