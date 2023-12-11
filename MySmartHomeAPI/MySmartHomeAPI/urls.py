"""
URL configuration for MySmartHomeAPI project.

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
from django.urls import include, path, re_path
from django.shortcuts import redirect
from rest_framework import routers
from MySmartHomeAPI.settings import API_VERSION
from API import views
from rest_framework.authtoken import views as auth_views
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

for user in User.objects.all():
    Token.objects.get_or_create(user=user)
API_URL_PREFIX = 'api/' + API_VERSION

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
router.register(r'kitchen/lights/keep_on', views.KitchenLightViewSet, basename='kitchen_light')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', lambda request: redirect('api/v1/', permanent=False)),
    path(API_URL_PREFIX+'/', include(router.urls)),
    path(API_URL_PREFIX+'/api-token-auth/', auth_views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('health/', include('health_check.urls')),
    
]

# urlpatterns += router.urls