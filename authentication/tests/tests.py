from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class RegisterTests(APITestCase):
    def test_register_creates_user(self):
        response = self.client.post('/auth/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SuperSecret123',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_duplicate_email_returns_400(self):
        User.objects.create_user(username='existing', email='test@example.com', password='pass12345')

        response = self.client.post('/auth/register/', {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SuperSecret123',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_missing_fields_returns_400(self):
        response = self.client.post('/auth/register/', {'email': '', 'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='SuperSecret123',
        )

    def test_login_success_sets_cookies(self):
        response = self.client.post('/auth/login/', {
            'username': 'test@example.com',
            'password': 'SuperSecret123',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        self.assertEqual(response.data['message'], 'Login successful')

    def test_login_wrong_password_returns_401(self):
        response = self.client.post('/auth/login/', {
            'username': 'test@example.com',
            'password': 'wrong-password',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_unknown_user_returns_401(self):
        response = self.client.post('/auth/login/', {
            'username': 'nobody@example.com',
            'password': 'whatever',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutTests(APITestCase):
    def test_logout_clears_cookies_and_returns_message(self):
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Logout successful')


class CreateDemoTests(APITestCase):
    def test_create_demo_creates_user_team_and_profile(self):
        response = self.client.post('/auth/create-demo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        self.assertEqual(response.data['message'], 'Demo account created successfully')
        self.assertIn('user', response.data)

    def test_create_demo_generates_unique_usernames(self):
        first = self.client.post('/auth/create-demo/')
        second = self.client.post('/auth/create-demo/')
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertNotEqual(first.data['user']['id'], second.data['user']['id'])


class RefreshTokenTests(APITestCase):
    def test_refresh_without_cookie_returns_400(self):
        response = self.client.post('/auth/token/refresh/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_with_invalid_token_returns_401(self):
        self.client.cookies['refresh_token'] = 'invalid-token'
        response = self.client.post('/auth/token/refresh/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_with_valid_token_sets_new_access_cookie(self):
        User.objects.create_user(username='u1@example.com', email='u1@example.com', password='pass12345')
        login_response = self.client.post('/auth/login/', {
            'username': 'u1@example.com',
            'password': 'pass12345',
        })
        self.client.cookies['refresh_token'] = login_response.cookies['refresh_token'].value

        response = self.client.post('/auth/token/refresh/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.cookies)
