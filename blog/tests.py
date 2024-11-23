from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Post, Category, Tag, Comment
from datetime import datetime
from django.utils import timezone

User = get_user_model()

class BlogTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category',
            description='Test Description'
        )
        
        # Create test tag
        self.tag = Tag.objects.create(
            name='Test Tag',
            slug='test-tag'
        )
        
        # Create test post
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Test Content',
            author=self.user,
            category=self.category,
            status='published',
            published_date=timezone.now()
        )
        self.post.tags.add(self.tag)

    def test_create_post(self):
        """Test creating a new blog post"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'New Content',
            'category': self.category.id,
            'tags': [self.tag.id],
            'status': 'draft'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_like_post(self):
        """Test liking a post"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-like', kwargs={'slug': self.post.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.post.likes.filter(id=self.user.id).exists())

    def test_comment_on_post(self):
        """Test commenting on a post"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-comments', kwargs={'post_pk': self.post.slug})
        data = {'content': 'Test Comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_unauthorized_access(self):
        """Test unauthorized access to protected endpoints"""
        url = reverse('post-list')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
