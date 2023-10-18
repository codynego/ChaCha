# In your tests.py file

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/auth/user/register/'
        self.valid_payload = {
            'first_name': 'test',
            'last_name': 'user',
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
   
        }
        self.invalid_payload = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }

    def test_valid_user_registration(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_invalid_user_registration(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duplicate_user_registration(self):
        # Create a user with the valid payload
        self.client.post(self.register_url, self.valid_payload, format='json')
        
        # Try to register a user with the same username and email
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
