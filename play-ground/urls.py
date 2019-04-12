"""play-ground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework import routers
from app import views, serializers


# django-restful-framework框架路由
router = routers.DefaultRouter()
router.register(r'users', serializers.UserInfoViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1.0/get_json_response/', views.JsonResponseView.as_view(), name='get_json_response'),
    path(r'api/v1.0/upload_file/', views.UploadFileView.as_view(), name='upload_file'),
    path(r'api/v1.0/resolve_json/', views.ResolveJsonView.as_view(), name='resolve_json'),
    path(r'api/v1.0/paginator_json/', views.PaginatorJsonView.as_view(), name='paginator_json'),
    path(r'restful/', include(router.urls)),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'api/user_jwt/', include('app.user_jwt.urls')),


]

