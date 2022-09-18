from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions

from .serializers import UserSerializer, GroupSerializer

# Create your views here.


class UserViewset(viewsets.ModelViewSet):
    
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewset(viewsets.ModelViewSet):
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
