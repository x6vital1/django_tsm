from django.urls import path
from tasks.api.api_views import TasksView

urlpatterns = [
    path('tasks/', TasksView.as_view(), name='tasks'),
]
