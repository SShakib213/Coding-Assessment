from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics, permissions
from .models import Post
from .serializers import PostSerializer, UserSerializer
from .permissions import IsOwner
from django.contrib.auth.models import User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsOwner()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
