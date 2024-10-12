"""
URL configuration for django_tsm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from .api_info import api_info
from rest_framework import permissions

schema_views = get_schema_view(
    api_info,
    url='http://127.0.0.1:8000/swagger/',
    public=True,
    permission_classes=[permissions.AllowAny],

)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
    path('swagger/', schema_views.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
