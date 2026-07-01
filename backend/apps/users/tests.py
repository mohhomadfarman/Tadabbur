import pytest
from rest_framework.test import APIClient

from .models import User
from .utils import generate_action_token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def no_real_email(monkeypatch):
    """Every test in this module hits register/forgot-password, which enqueue a
    Celery email task — stub `.delay` so tests never need a live broker."""
    monkeypatch.setattr('apps.users.views.send_transactional_email.delay', lambda *a, **k: None)


@pytest.fixture(autouse=True)
def clean_test_users():
    """MongoEngine writes aren't wrapped in Django's per-test transaction, so
    @example.com users created by this module would otherwise leak across
    test runs and collide on the unique email/username indexes."""
    yield
    User.objects(email__endswith='@example.com').delete()


@pytest.mark.django_db
class TestAuthEndpoints:

    def test_register_success(self, client):
        response = client.post('/api/v1/auth/register/', {
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'strongpass123',
            'full_name': 'Test User',
        }, format='json')
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == 'test@example.com'

    def test_register_duplicate_email(self, client):
        data = {'email': 'dup@example.com', 'username': 'user1', 'password': 'strongpass123'}
        client.post('/api/v1/auth/register/', data, format='json')
        response = client.post('/api/v1/auth/register/', {**data, 'username': 'user2'}, format='json')
        assert response.status_code == 400

    def test_login_success(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'login@example.com',
            'username': 'loginuser',
            'password': 'strongpass123',
        }, format='json')
        response = client.post('/api/v1/auth/login/', {
            'email': 'login@example.com',
            'password': 'strongpass123',
        }, format='json')
        assert response.status_code == 200
        assert 'access' in response.data

    def test_login_wrong_password(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'wrong@example.com',
            'username': 'wronguser',
            'password': 'correctpass123',
        }, format='json')
        response = client.post('/api/v1/auth/login/', {
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
        }, format='json')
        assert response.status_code == 401

    def test_profile_requires_auth(self, client):
        response = client.get('/api/v1/auth/profile/')
        assert response.status_code == 401

    def test_profile_with_token(self, client):
        reg = client.post('/api/v1/auth/register/', {
            'email': 'profile@example.com',
            'username': 'profileuser',
            'password': 'strongpass123',
        }, format='json')
        token = reg.data['access']
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.get('/api/v1/auth/profile/')
        assert response.status_code == 200
        assert response.data['email'] == 'profile@example.com'


@pytest.mark.django_db
class TestEmailVerification:

    def test_register_leaves_user_unverified(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'unverified@example.com', 'username': 'unverifieduser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='unverified@example.com')
        assert user.is_verified is False

    def test_verify_email_success(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'verify@example.com', 'username': 'verifyuser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='verify@example.com')
        token = generate_action_token(user, 'verify_email', minutes=60)

        response = client.post('/api/v1/auth/verify-email/', {'token': token}, format='json')
        assert response.status_code == 200
        user.reload()
        assert user.is_verified is True

    def test_verify_email_invalid_token(self, client):
        response = client.post('/api/v1/auth/verify-email/', {'token': 'not-a-real-token'}, format='json')
        assert response.status_code == 400

    def test_verify_email_wrong_action_token_rejected(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'wrongaction@example.com', 'username': 'wrongactionuser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='wrongaction@example.com')
        reset_token = generate_action_token(user, 'reset_password', minutes=30)

        response = client.post('/api/v1/auth/verify-email/', {'token': reset_token}, format='json')
        assert response.status_code == 400
        user.reload()
        assert user.is_verified is False

    def test_resend_verification_requires_auth(self, client):
        response = client.post('/api/v1/auth/resend-verification/')
        assert response.status_code == 401

    def test_resend_verification_when_already_verified(self, client):
        reg = client.post('/api/v1/auth/register/', {
            'email': 'already@example.com', 'username': 'alreadyuser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='already@example.com')
        user.is_verified = True
        user.save()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {reg.data['access']}")

        response = client.post('/api/v1/auth/resend-verification/')
        assert response.status_code == 200
        assert 'already verified' in response.data['detail']


@pytest.mark.django_db
class TestForgotResetPassword:

    def test_forgot_password_always_returns_200(self, client):
        response = client.post('/api/v1/auth/forgot-password/', {'email': 'nobody@example.com'}, format='json')
        assert response.status_code == 200

    def test_reset_password_success(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'reset@example.com', 'username': 'resetuser', 'password': 'oldpassword1',
        }, format='json')
        user = User.objects.get(email='reset@example.com')
        token = generate_action_token(user, 'reset_password', minutes=30)

        response = client.post('/api/v1/auth/reset-password/', {'token': token, 'password': 'newpassword1'}, format='json')
        assert response.status_code == 200

        login = client.post('/api/v1/auth/login/', {'email': 'reset@example.com', 'password': 'newpassword1'}, format='json')
        assert login.status_code == 200

    def test_reset_password_invalid_token(self, client):
        response = client.post('/api/v1/auth/reset-password/', {'token': 'garbage', 'password': 'newpassword1'}, format='json')
        assert response.status_code == 400

    def test_reset_password_wrong_action_token_rejected(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'verifynotreset@example.com', 'username': 'verifynotresetuser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='verifynotreset@example.com')
        verify_token = generate_action_token(user, 'verify_email', minutes=60)

        response = client.post('/api/v1/auth/reset-password/', {'token': verify_token, 'password': 'newpassword1'}, format='json')
        assert response.status_code == 400

    def test_reset_password_too_short(self, client):
        client.post('/api/v1/auth/register/', {
            'email': 'shortpass@example.com', 'username': 'shortpassuser', 'password': 'strongpass123',
        }, format='json')
        user = User.objects.get(email='shortpass@example.com')
        token = generate_action_token(user, 'reset_password', minutes=30)

        response = client.post('/api/v1/auth/reset-password/', {'token': token, 'password': 'short'}, format='json')
        assert response.status_code == 400
