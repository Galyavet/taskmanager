from django.urls import path
from .views import ProjectAPIView, ProjectDetailAPIView


urlpatterns = [
    path('projects/', ProjectAPIView.as_view(), name='get_projects'),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view(), name='get_projects_details'),


]
