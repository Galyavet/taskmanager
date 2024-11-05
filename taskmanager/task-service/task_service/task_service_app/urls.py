from django.urls import path
from .views import TaskDetailAPIView, TaskAPIView


urlpatterns = [
    path('tasks/', TaskAPIView.as_view(), name='get_tasks'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='get_tasks_details'),


]
