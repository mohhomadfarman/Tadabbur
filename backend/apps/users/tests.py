import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


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
        assert response.status_code == 403

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
