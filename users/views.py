from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from blog.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def posts(self, request, pk=None):
        user = self.get_object()
        posts = user.posts.all()
        from blog.serializers import PostSerializer
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def liked_posts(self, request, pk=None):
        user = self.get_object()
        posts = user.liked_posts.all()
        from blog.serializers import PostSerializer
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
