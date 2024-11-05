import requests
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import UserSerializer


class UserAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class UsersAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserAPIListPagination

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        name = request.query_params.get('name', None)\

        filter_kwargs = {}
        if email:
            filter_kwargs['email__icontains'] = email
        if name:
            filter_kwargs['first_name__icontains'] = name

        queryset = self.queryset.filter(**filter_kwargs)
        page = self.paginate_queryset(queryset)
        serializer = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer.data)


class UsersDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


@api_view(('GET',))
def get_current_user_info(request):
    jwt_token = request.headers.get('Authorization')
    try:
        response = requests.get(
            'http://auth-service:8000/profile/',
            headers={'Authorization': jwt_token}
        )
        response.raise_for_status()
        user_data = response.json()
    except requests.RequestException as e:
        return Response({'error': 'Failed to fetch userinfo'}, status=500)

    return JsonResponse(user_data, safe=False)
