"""Shared track-completion detection. Used by the feedback prompt (apps.feedback)
and the badge award evaluator (apps.badges). Mirrors the math in
TrackProgressView so all three agree on what "track complete" means."""
from apps.lessons.models import Lesson
from apps.curriculum.models import Track, Subject
from .models import LessonProgress


def track_completion(user, track_slug):
    """Return (completed_count, total_count) of published lessons across the
    published subjects of a published track, for `user`. total==0 if the track
    doesn't exist / has no published lessons."""
    track = Track.objects(slug=track_slug, is_published=True).first()
    if not track:
        return 0, 0

    # All completed slugs (not filtered by track_slug — older records may have had
    # an empty track_slug; match TrackProgressView's approach).
    all_completed = set(
        LessonProgress.objects(user=user, completed=True).scalar('lesson_slug')
    )

    total = 0
    done = 0
    for subj in Subject.objects(track=track, is_published=True):
        lessons = list(Lesson.objects(subject=subj, status='published').scalar('slug'))
        total += len(lessons)
        done += sum(1 for s in lessons if s in all_completed)
    return done, total


def track_is_complete(user, track_slug):
    """True if every published lesson of the track is completed by `user`."""
    done, total = track_completion(user, track_slug)
    return total > 0 and done == total
