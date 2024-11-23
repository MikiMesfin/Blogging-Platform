from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Category, Tag, Comment
from .serializers import (
    PostSerializer, CategorySerializer, 
    TagSerializer, CommentSerializer
)
from .permissions import IsAuthorOrReadOnly
from django.utils import timezone
from .decorators import rate_limit

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'tags', 'status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_date', 'published_date']
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.all()
        return Post.objects.filter(status='published')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    @rate_limit('post_like', limit=10, period=3600)  # 10 likes per hour
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        
        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
            post.likes.add(user)
            return Response({'status': 'liked'})

    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        post = self.get_object()
        if post.author != request.user:
            return Response(
                {'error': 'Only the author can publish this post'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.status = 'published'
        post.published_date = timezone.now()
        post.save()
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post_id=self.kwargs['post_pk']
        )
