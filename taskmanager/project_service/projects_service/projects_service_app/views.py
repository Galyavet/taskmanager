import requests
from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Project
from .serializers import ProjectSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner_email == request.user.email


class ProjectAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if request.user.is_staff:
            queryset = self.queryset.all()
        else:
            queryset = self.queryset.filter(owner_email=request.user.email)

        serializer = ProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        jwt_token = request.headers.get('Authorization')
        task_id = request.data['task_id']
        try:
            response = requests.get(
                f'http://task-service:8000/tasks/{task_id}/',
                headers={'Authorization': jwt_token}
            )
            response.raise_for_status()
            books_data = response.json()
        except requests.RequestException as e:
            return Response({'error': 'Failed to fetch tasks'}, status=500)

        project = Project.objects.create(
            owner_email=request.user.email,
            tasks=books_data
        )
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
