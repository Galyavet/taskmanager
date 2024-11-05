from django.contrib.sites import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import viewsets, status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner_email == request.user.email


class TaskAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(20))
    @method_decorator(vary_on_headers('Authorization'))
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(owner_email=request.user.email)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
