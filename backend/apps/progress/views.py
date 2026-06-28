from datetime import datetime, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.lessons.models import Lesson
from apps.curriculum.models import Track, Subject
from apps.common.permissions import section_required
from .models import LessonProgress, UserProgress, QuizAttempt


def _get_or_create_user_progress(user):
    up = UserProgress.objects(user=user).first()
    if not up:
        up = UserProgress(user=user, enrolled_tracks=[], updated_at=datetime.now(timezone.utc))
        up.save()
    return up


def _valid_language(code):
    """Return code if it's a currently-enabled translation language, else ''."""
    code = (code or '').strip()
    if not code:
        return ''
    from apps.translations.models import TranslationSettings
    enabled = {l.code for l in TranslationSettings.get_solo().enabled_languages()}
    return code if code in enabled else ''


def _set_track_language(up, track_slug, code):
    """Store (or clear) the per-track reading language. Returns the stored value."""
    langs = dict(up.track_languages or {})
    valid = _valid_language(code)
    if valid:
        langs[track_slug] = valid
    else:
        langs.pop(track_slug, None)
    up.track_languages = langs
    return langs.get(track_slug, '')


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
        track_languages = {}
        current_streak = 0
        longest_streak = 0
        last_activity = None

        if up:
            enrolled_tracks = up.enrolled_tracks or []
            track_languages = up.track_languages or {}
            current_streak = up.current_streak_days or 0
            longest_streak = up.longest_streak_days or 0
            last_activity = up.last_activity_date.isoformat() if up.last_activity_date else None

        # Continue learning: find the next uncompleted lesson after the last activity
        continue_learning = None
        completed_set = set(completed_slugs)
        last_lp = LessonProgress.objects(
            user=request.user, completed=True
        ).order_by('-completed_at').first()

        if last_lp:
            try:
                last_lesson = last_lp.lesson
                # Try next lesson in same subject that isn't completed yet
                nxt = Lesson.objects(
                    subject=last_lesson.subject,
                    status='published',
                    order__gt=last_lesson.order,
                ).order_by('order').first()

                if nxt and nxt.slug in completed_set:
                    nxt = None  # already done, don't suggest it

                target = nxt if nxt else None

                # If nothing left in this subject, fall back to last lesson
                # only if it itself is NOT completed (shouldn't happen, but guard it)
                if target is None and last_lesson.slug not in completed_set:
                    target = last_lesson

                if target:
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
            'track_languages': track_languages,
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

        language = ''
        if 'language' in request.data:
            language = _set_track_language(up, track_slug, request.data.get('language'))

        up.updated_at = datetime.now(timezone.utc)
        up.save()
        return Response({'enrolled': True, 'track_slug': track_slug, 'language': language})

    def delete(self, request, track_slug):
        up = UserProgress.objects(user=request.user).first()
        if up and track_slug in up.enrolled_tracks:
            up.enrolled_tracks.remove(track_slug)
            up.updated_at = datetime.now(timezone.utc)
            up.save()
        return Response({'enrolled': False, 'track_slug': track_slug})


class SetTrackLanguageView(APIView):
    """Change the reading language for a track (the lesson-page switcher)."""
    permission_classes = [IsAuthenticated]

    def post(self, request, track_slug):
        up = _get_or_create_user_progress(request.user)
        language = _set_track_language(up, track_slug, request.data.get('language'))
        up.updated_at = datetime.now(timezone.utc)
        up.save()
        return Response({'track_slug': track_slug, 'language': language})


class TrackProgressView(APIView):
    """Completion breakdown for one enrolled track."""
    permission_classes = [IsAuthenticated]

    def get(self, request, track_slug):
        track = Track.objects(slug=track_slug, is_published=True).first()
        if not track:
            return Response({'detail': 'Track not found.'}, status=status.HTTP_404_NOT_FOUND)

        subjects = Subject.objects(track=track, is_published=True).order_by('order')

        # Use all completed lesson slugs for the user (not filtered by track_slug,
        # because track_slug may have been empty when older records were created).
        all_completed = set(
            LessonProgress.objects(
                user=request.user, completed=True
            ).scalar('lesson_slug')
        )

        total_all = 0
        completed_all = 0
        subjects_data = []

        for subj in subjects:
            lessons = list(Lesson.objects(subject=subj, status='published').scalar('slug'))
            total = len(lessons)
            done = sum(1 for s in lessons if s in all_completed)
            total_all += total
            completed_all += done
            subjects_data.append({
                'subject_slug': subj.slug,
                'subject_title': subj.title,
                'total_lessons': total,
                'completed_lessons': done,
                'percent': round(done / total * 100) if total else 0,
            })

        return Response({
            'track_slug': track_slug,
            'track_title': track.title,
            'total_lessons': total_all,
            'completed_lessons': completed_all,
            'percent': round(completed_all / total_all * 100) if total_all else 0,
            'subjects': subjects_data,
        })


class SaveQuizAnswerView(APIView):
    """Save a user's quiz answer for a specific block in a lesson."""
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        lesson = Lesson.objects(slug=slug, status='published').first()
        if not lesson:
            return Response({'detail': 'Lesson not found.'}, status=status.HTTP_404_NOT_FOUND)

        block_order = request.data.get('block_order')
        selected_index = request.data.get('selected_index')
        if block_order is None or selected_index is None:
            return Response({'detail': 'block_order and selected_index are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Find the quiz block for metadata
        quiz_block = next(
            (b for b in lesson.content_blocks if b.order == block_order and b.type == 'quiz'),
            None
        )
        question = ''
        selected_answer = ''
        correct_index = None
        is_correct = False

        if quiz_block:
            question = quiz_block.body.get('question', '')
            options = quiz_block.body.get('options', [])
            correct_index = quiz_block.body.get('correct')
            selected_answer = options[selected_index] if 0 <= selected_index < len(options) else ''
            is_correct = (selected_index == correct_index)

        # Upsert — one record per user per lesson per block
        attempt = QuizAttempt.objects(
            user=request.user,
            lesson_slug=slug,
            block_order=block_order,
        ).first()

        if attempt:
            attempt.selected_index = selected_index
            attempt.selected_answer = selected_answer
            attempt.is_correct = is_correct
            attempt.attempted_at = datetime.now(timezone.utc)
        else:
            attempt = QuizAttempt(
                user=request.user,
                lesson_slug=slug,
                block_order=block_order,
                question=question,
                selected_index=selected_index,
                selected_answer=selected_answer,
                correct_index=correct_index,
                is_correct=is_correct,
                attempted_at=datetime.now(timezone.utc),
            )
        attempt.save()

        return Response({'saved': True, 'is_correct': is_correct})


class AdminLessonStatsView(APIView):
    """Admin: completion counts + quiz answer breakdown per lesson."""
    permission_classes = [section_required('analytics')]

    def get(self, request):
        lesson_slug = request.query_params.get('lesson')

        if lesson_slug:
            # Per-lesson detail: who completed it + quiz answers
            completed_users = LessonProgress.objects(lesson_slug=lesson_slug, completed=True)
            completion_count = completed_users.count()

            # Quiz answer breakdown grouped by block_order
            attempts = QuizAttempt.objects(lesson_slug=lesson_slug)
            quiz_stats = {}
            for a in attempts:
                key = str(a.block_order)
                if key not in quiz_stats:
                    quiz_stats[key] = {
                        'question': a.question,
                        'correct_index': a.correct_index,
                        'total_attempts': 0,
                        'correct_count': 0,
                        'answer_distribution': {},
                    }
                quiz_stats[key]['total_attempts'] += 1
                if a.is_correct:
                    quiz_stats[key]['correct_count'] += 1
                ans_key = str(a.selected_index)
                quiz_stats[key]['answer_distribution'][ans_key] = \
                    quiz_stats[key]['answer_distribution'].get(ans_key, 0) + 1

            return Response({
                'lesson_slug': lesson_slug,
                'completion_count': completion_count,
                'quiz_stats': quiz_stats,
            })

        # Summary: completion count per lesson slug
        pipeline = [
            {'$match': {'completed': True}},
            {'$group': {'_id': '$lesson_slug', 'count': {'$sum': 1}}},
            {'$sort': {'count': -1}},
            {'$limit': 50},
        ]
        results = list(LessonProgress.objects.aggregate(pipeline))
        return Response([{'lesson_slug': r['_id'], 'completion_count': r['count']} for r in results])
