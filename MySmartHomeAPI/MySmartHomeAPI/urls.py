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
from django.urls import include, path
from rest_framework import routers
from MySmartHomeAPI.settings import API_VERSION
from API import views
API_URL_PREFIX = 'api/' + API_VERSION

router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)
# router.register(r'kitchen/lights/keep_on/<int:val>/', )

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/'+API_VERSION+'/', include(router.urls)),
    path(API_URL_PREFIX + '/kitchen/lights/keep_on/', views.kitchen_lights_keep_on),
    path(API_URL_PREFIX +'/kitchen/lights/keep_on/<int:val>/', views.kitchen_lights_keep_on),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

urlpatterns += router.urls