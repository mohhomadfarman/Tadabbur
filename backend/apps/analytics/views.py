from datetime import datetime, timezone, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.permissions import section_required
from apps.users.models import User
from apps.curriculum.models import Track, Subject
from apps.lessons.models import Lesson, LessonView
from apps.progress.models import LessonProgress, UserProgress
from apps.feedback.models import TrackFeedback


def _zero_fill_days(counts, num_days):
    """counts: {'YYYY-MM-DD': n}. Returns a continuous list, oldest first."""
    today = datetime.now(timezone.utc).date()
    out = []
    for i in range(num_days - 1, -1, -1):
        d = today - timedelta(days=i)
        key = d.isoformat()
        out.append({'date': key, 'count': counts.get(key, 0)})
    return out


def _signups_series(days):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days - 1)
    cutoff = cutoff.replace(hour=0, minute=0, second=0, microsecond=0)
    pipeline = [
        {'$match': {'created_at': {'$gte': cutoff}}},
        {'$group': {
            '_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$created_at'}},
            'count': {'$sum': 1},
        }},
    ]
    counts = {r['_id']: r['count'] for r in User.objects.aggregate(pipeline)}
    return _zero_fill_days(counts, days)


def _readers_series(days=7):
    cutoff_date = datetime.now(timezone.utc).date() - timedelta(days=days - 1)
    cutoff_dt = datetime.combine(cutoff_date, datetime.min.time())
    pipeline = [
        {'$match': {'view_date': {'$gte': cutoff_dt}}},
        {'$group': {'_id': '$view_date', 'users': {'$addToSet': '$user'}}},
        {'$project': {'count': {'$size': '$users'}}},
    ]
    counts = {}
    for r in LessonView.objects.aggregate(pipeline):
        d = r['_id']
        key = (d.date() if hasattr(d, 'date') else d).isoformat()
        counts[key] = r['count']
    return _zero_fill_days(counts, days)


def _track_readers_series(track_slug, days=30):
    cutoff_date = datetime.now(timezone.utc).date() - timedelta(days=days - 1)
    cutoff_dt = datetime.combine(cutoff_date, datetime.min.time())
    pipeline = [
        {'$match': {'view_date': {'$gte': cutoff_dt}, 'track_slug': track_slug}},
        {'$group': {'_id': '$view_date', 'users': {'$addToSet': '$user'}}},
        {'$project': {'count': {'$size': '$users'}}},
    ]
    counts = {}
    for r in LessonView.objects.aggregate(pipeline):
        d = r['_id']
        key = (d.date() if hasattr(d, 'date') else d).isoformat()
        counts[key] = r['count']
    return _zero_fill_days(counts, days)


def _top_tracks(limit=5):
    pipeline = [
        {'$match': {'completed': True, 'track_slug': {'$nin': [None, '']}}},
        {'$group': {'_id': '$track_slug', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': limit},
    ]
    return [{'track_slug': r['_id'], 'completions': r['count']} for r in LessonProgress.objects.aggregate(pipeline)]


class AdminOverviewStatsView(APIView):
    """Single combined payload for the admin Overview dashboard — stat cards,
    signups-over-time and distinct-readers-over-time series, and a top-tracks
    list. Kept as one endpoint since every piece is consumed on the same page
    load; per-track/per-lesson breakdowns already live at /admin/analytics and
    /admin/feedback and are linked out to rather than duplicated here."""
    permission_classes = [section_required('analytics')]

    def get(self, request):
        days = request.query_params.get('days')
        try:
            days = max(1, min(int(days), 90))
        except (TypeError, ValueError):
            days = 30

        active_cutoff = datetime.now(timezone.utc).date() - timedelta(days=6)
        active_users_7d = len(LessonView.objects(view_date__gte=active_cutoff).distinct('user'))

        feedback_pipeline = [
            {'$group': {'_id': None, 'avg': {'$avg': '$rating'}, 'count': {'$sum': 1}}},
        ]
        fb_rows = list(TrackFeedback.objects.aggregate(feedback_pipeline))
        feedback_average = round(fb_rows[0]['avg'], 2) if fb_rows and fb_rows[0]['avg'] is not None else 0
        feedback_count = fb_rows[0]['count'] if fb_rows else 0

        return Response({
            'total_users': User.objects.count(),
            'verified_users': User.objects(is_verified=True).count(),
            'published_tracks': Track.objects(is_published=True).count(),
            'published_subjects': Subject.objects(is_published=True).count(),
            'published_lessons': Lesson.objects(status='published').count(),
            'total_lessons_completed': LessonProgress.objects(completed=True).count(),
            'active_users_7d': active_users_7d,
            'feedback_average': feedback_average,
            'feedback_count': feedback_count,
            'top_tracks': _top_tracks(),
            'signups_series': _signups_series(days),
            'readers_series': _readers_series(),
        })


class AdminTrackStatsView(APIView):
    """Per-track analytics for the Track detail admin page: completion funnel
    (enrolled / in-progress / completed), last-opened, and a daily readers
    chart scoped to this one track."""
    permission_classes = [section_required('analytics')]

    def get(self, request, track_slug):
        track = Track.objects(slug=track_slug).first()
        if not track:
            return Response({'detail': 'Not found.'}, status=404)

        days = request.query_params.get('days')
        try:
            days = max(1, min(int(days), 90))
        except (TypeError, ValueError):
            days = 30

        total_lessons = 0
        for subj in Subject.objects(track=track, is_published=True):
            total_lessons += Lesson.objects(subject=subj, status='published').count()

        enrolled_count = UserProgress.objects(enrolled_tracks=track_slug).count()

        pipeline = [
            {'$match': {'track_slug': track_slug, 'completed': True}},
            {'$group': {'_id': '$user', 'c': {'$sum': 1}}},
        ]
        per_user_counts = [r['c'] for r in LessonProgress.objects.aggregate(pipeline)]

        if total_lessons > 0:
            completed_count = sum(1 for c in per_user_counts if c >= total_lessons)
            in_progress_count = sum(1 for c in per_user_counts if 0 < c < total_lessons)
        else:
            completed_count = 0
            in_progress_count = 0
        not_started_count = max(0, enrolled_count - completed_count - in_progress_count)

        last_view = LessonView.objects(track_slug=track_slug).order_by('-viewed_at').first()
        last_opened = None
        if last_view:
            last_opened = {
                'viewed_at': last_view.viewed_at.isoformat(),
                'user_name': last_view.user.full_name or last_view.user.username,
            }

        return Response({
            'track_slug': track_slug,
            'total_lessons': total_lessons,
            'enrolled_count': enrolled_count,
            'completed_count': completed_count,
            'in_progress_count': in_progress_count,
            'not_started_count': not_started_count,
            'last_opened': last_opened,
            'readers_series': _track_readers_series(track_slug, days),
        })
