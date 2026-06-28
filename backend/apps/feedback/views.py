from datetime import datetime, timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.permissions import section_required
from apps.features.service import feature_enabled
from .models import TrackFeedback


def _iso(dt):
    return dt.isoformat() if dt else None


class SubmitFeedbackView(APIView):
    """Learner submits a rating (1–5) + optional comment for a completed track.
    Idempotent per (user, track) — re-submitting updates the existing record."""
    permission_classes = [IsAuthenticated]

    def post(self, request, track_slug):
        if not feature_enabled('track_feedback', request.user):
            return Response({'detail': 'Feedback is not enabled.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            rating = int(request.data.get('rating'))
        except (TypeError, ValueError):
            return Response({'rating': 'A rating between 1 and 5 is required.'}, status=status.HTTP_400_BAD_REQUEST)
        if rating < 1 or rating > 5:
            return Response({'rating': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)

        comment = (request.data.get('comment') or '').strip()[:2000]
        now = datetime.now(timezone.utc)

        fb = TrackFeedback.objects(user=request.user, track_slug=track_slug).first()
        if not fb:
            fb = TrackFeedback(user=request.user, track_slug=track_slug, created_at=now)
        fb.rating = rating
        fb.comment = comment
        fb.updated_at = now
        try:
            fb.save()
        except Exception:
            # unique-index race — fetch and update the winner
            fb = TrackFeedback.objects(user=request.user, track_slug=track_slug).first()
            if fb:
                fb.rating = rating
                fb.comment = comment
                fb.updated_at = now
                fb.save()
        return Response({'submitted': True, 'track_slug': track_slug, 'rating': rating})


class MyTrackFeedbackView(APIView):
    """Whether the current user has already given feedback for a track — drives the
    'don't show the prompt again' guard."""
    permission_classes = [IsAuthenticated]

    def get(self, request, track_slug):
        fb = TrackFeedback.objects(user=request.user, track_slug=track_slug).first()
        if not fb:
            return Response({'submitted': False})
        return Response({'submitted': True, 'rating': fb.rating, 'comment': fb.comment})


class AdminFeedbackListView(APIView):
    """Admin: per-track aggregate (count, average, distribution) + recent comments."""
    permission_classes = [section_required('feedback')]

    def get(self, request):
        # Aggregate count + average + rating distribution per track in one pass.
        pipeline = [
            {'$group': {
                '_id': '$track_slug',
                'count': {'$sum': 1},
                'avg': {'$avg': '$rating'},
                'r1': {'$sum': {'$cond': [{'$eq': ['$rating', 1]}, 1, 0]}},
                'r2': {'$sum': {'$cond': [{'$eq': ['$rating', 2]}, 1, 0]}},
                'r3': {'$sum': {'$cond': [{'$eq': ['$rating', 3]}, 1, 0]}},
                'r4': {'$sum': {'$cond': [{'$eq': ['$rating', 4]}, 1, 0]}},
                'r5': {'$sum': {'$cond': [{'$eq': ['$rating', 5]}, 1, 0]}},
            }},
            {'$sort': {'count': -1}},
        ]
        rows = list(TrackFeedback.objects.aggregate(pipeline))

        result = []
        for r in rows:
            slug = r['_id']
            # Up to 10 most recent comments for this track.
            comments = []
            for fb in TrackFeedback.objects(track_slug=slug, comment__ne='').order_by('-updated_at').limit(10):
                comments.append({'rating': fb.rating, 'comment': fb.comment, 'at': _iso(fb.updated_at)})
            result.append({
                'track_slug': slug,
                'count': r['count'],
                'average': round(r['avg'], 2) if r['avg'] is not None else 0,
                'distribution': {'1': r['r1'], '2': r['r2'], '3': r['r3'], '4': r['r4'], '5': r['r5']},
                'recent_comments': comments,
            })
        return Response(result)
