"""Badge award evaluation. Called after a lesson/track completion (from
MarkCompleteView) to grant any newly-earned badges. Designed to be a safe no-op
when the `badges` feature is disabled, and to never raise into the caller."""
from datetime import datetime, timezone

from apps.features.service import feature_enabled
from apps.progress.models import LessonProgress, UserProgress
from apps.progress.completion import track_is_complete
from apps.emails.transactional import send_transactional_email, badge_earned_email_body
from .models import Badge, UserBadge


def _notify_badge_earned(user, badge):
    try:
        send_transactional_email.delay(f'You earned a badge: {badge.name}', badge_earned_email_body(badge), user.email)
    except Exception:
        pass  # never let a notification failure break badge awarding


def _criteria_met(badge, user):
    t = badge.criteria_type
    if t == 'track_complete':
        return bool(badge.criteria_value) and track_is_complete(user, badge.criteria_value)
    if t == 'lessons_count':
        try:
            need = int(badge.criteria_value)
        except (TypeError, ValueError):
            return False
        return LessonProgress.objects(user=user, completed=True).count() >= need
    if t == 'streak':
        try:
            need = int(badge.criteria_value)
        except (TypeError, ValueError):
            return False
        up = UserProgress.objects(user=user).first()
        return bool(up) and (up.current_streak_days or 0) >= need
    # 'manual' (or unknown) is never auto-awarded.
    return False


def evaluate_awards(user):
    """Grant any active, auto-criteria badges the user now qualifies for.
    Returns the list of newly-created UserBadge documents (may be empty)."""
    if not feature_enabled('badges', user):
        return []

    newly = []
    # Badges the user already has — skip those.
    owned = set(
        str(bid) for bid in
        UserBadge._get_collection().distinct('badge', {'user': user.id})
    )
    for badge in Badge.objects(is_active=True, criteria_type__ne='manual'):
        if str(badge.id) in owned:
            continue
        if not _criteria_met(badge, user):
            continue
        try:
            ub = UserBadge(user=user, badge=badge, awarded_at=datetime.now(timezone.utc)).save()
            newly.append(ub)
            _notify_badge_earned(user, badge)
        except Exception:
            pass  # unique-index race — already awarded
    return newly


def grant_badge(user, badge):
    """Explicitly award `badge` to `user` (used for manual badges). Idempotent."""
    existing = UserBadge.objects(user=user, badge=badge).first()
    if existing:
        return existing
    try:
        ub = UserBadge(user=user, badge=badge, awarded_at=datetime.now(timezone.utc)).save()
        _notify_badge_earned(user, badge)
        return ub
    except Exception:
        return UserBadge.objects(user=user, badge=badge).first()
