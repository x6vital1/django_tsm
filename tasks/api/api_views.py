from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import GenericAPIView
import django_filters

from tasks.models.task import Tasks

from .serializers import TasksSerializer


class TasksFiltersSet(django_filters.FilterSet):
    class Meta:
        model = Tasks
        fields = {
            'title': ['exact'],
            'difficulty': ['exact', 'icontains'],

        }

class TasksView(GenericAPIView):
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    filterset_class = TasksFiltersSet
    search_fields = ['title', 'description']
    ordering_fields = ['__all__']

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return Tasks.objects.all()
        return Tasks.objects.filter(id=self.request.user.id)

    @swagger_auto_schema(responses={200: TasksSerializer(many=True)})
    def get(self, request):
        tasks = self.get_queryset()
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary='Create a task',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'difficulty': openapi.Schema(type=openapi.TYPE_STRING),
                'deadline': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response('Created', TasksSerializer),
            400: openapi.Response('Bad Request', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(type=openapi.TYPE_STRING, description="Error message"),
                }
            ))
        }
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)