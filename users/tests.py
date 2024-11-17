from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'bio': 'Test bio'
        }
        self.user = User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existing123'
        )

    def test_create_user(self):
        """Test creating a new user"""
        url = reverse('user-list')
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login(self):
        """Test user login and token generation"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'existinguser',
            'password': 'existing123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_profile(self):
        """Test retrieving and updating user profile"""
        self.client.force_authenticate(user=self.user)
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        
        # Test GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'existinguser')
        
        # Test PATCH
        update_data = {'bio': 'Updated bio'}
        response = self.client.patch(url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['bio'], 'Updated bio')
