from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import GenericAPIView

from users.models import CustomUser, UserProfile

from .serializers import CustomUserSerializer, UserProfileSerializer


class UsersAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def get(self, request):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class UserProfileAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(id=self.request.user.id)

    def get(self, request):
        user_profile = self.get_queryset()
        serializer = self.get_serializer(user_profile, many=True)
        return Response(serializer.data)
