from django.urls import path
from .views import MyObtainTokenPairView, RegisterView, ProfileAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('profile/', ProfileAPIView.as_view(), name='profile_user'),
]
