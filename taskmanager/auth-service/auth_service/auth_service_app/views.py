from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import MyTokenObtainPairSerializer, RegisterSerializer, ProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        queryset = User.objects.filter(email=self.request.data['email'])
        if queryset.exists():
            raise ValidationError({'email': 'This e-mail already signed up'})
        serializer.save(user=self.request.user)


class ProfileAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response({'user_about': serializer.data})

