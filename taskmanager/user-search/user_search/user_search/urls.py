"""
URL configuration for user_search project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user_search_app.views import *


urlpatterns = [
    path('admin/users/', admin.site.urls),
    path('users/', UsersAPIView.as_view(), name='get_users'),
    path('users/<int:pk>/', UsersDetailAPIView.as_view(), name='get_user_details'),
    path('users/me/', get_current_user_info, name='get_user_info')
]
