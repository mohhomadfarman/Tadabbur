import pytest
from rest_framework.test import APIClient

from apps.users.models import User
from .models import Badge, UserBadge
from .awards import grant_badge


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def no_real_email(monkeypatch):
    monkeypatch.setattr('apps.badges.awards.send_transactional_email.delay', lambda *a, **k: None)


@pytest.fixture
def user():
    # MongoEngine writes aren't wrapped in Django's per-test transaction, so
    # clean up explicitly rather than relying on test-DB rollback.
    User.objects(email='learner@example.com').delete()
    u = User(email='learner@example.com', username='learner')
    u.set_password('strongpass123')
    u.save()
    yield u
    UserBadge.objects(user=u).delete()
    u.delete()


@pytest.fixture
def manual_badge():
    Badge.objects(key='first-steps').delete()
    b = Badge(key='first-steps', name='First Steps', criteria_type='manual').save()
    yield b
    UserBadge.objects(badge=b).delete()
    b.delete()


@pytest.mark.django_db
class TestGrantBadge:

    def test_grant_badge_creates_user_badge(self, user, manual_badge):
        grant_badge(user, manual_badge)
        assert UserBadge.objects(user=user, badge=manual_badge).count() == 1

    def test_grant_badge_is_idempotent(self, user, manual_badge):
        grant_badge(user, manual_badge)
        grant_badge(user, manual_badge)
        assert UserBadge.objects(user=user, badge=manual_badge).count() == 1

    def test_grant_badge_sends_email(self, user, manual_badge, monkeypatch):
        calls = []
        monkeypatch.setattr('apps.badges.awards.send_transactional_email.delay', lambda *a, **k: calls.append(a))
        grant_badge(user, manual_badge)
        assert len(calls) == 1
        assert user.email in calls[0]

    def test_admin_grant_endpoint_requires_section(self, client, user, manual_badge):
        client.credentials()  # anonymous
        response = client.post(f'/api/v1/badges/admin/{manual_badge.id}/grant/', {'user_id': str(user.id)}, format='json')
        assert response.status_code in (401, 403)
