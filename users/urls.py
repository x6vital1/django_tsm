from django.urls import path
from users.api.api_views import UsersAPIView, UserProfileAPIView


urlpatterns = [
    path('users/', UsersAPIView.as_view()),
    path('profiles/', UserProfileAPIView.as_view()),
]