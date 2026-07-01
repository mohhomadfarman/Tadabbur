from datetime import datetime, timezone, timedelta

from rest_framework.views import APIView
from rest_framework.response import Response

from apps.common.permissions import section_required
from apps.users.models import User
from apps.curriculum.models import Track, Subject
from apps.lessons.models import Lesson, LessonView
from apps.progress.models import LessonProgress
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
