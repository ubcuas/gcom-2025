"""
URL configuration for gcom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from rest_framework.routers import DefaultRouter
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from nav.views import WaypointViewset
from odlc.views import GroundObjectViewset, CameraUploadAPIView


router = DefaultRouter()
router.register(r'waypoint', WaypointViewset, basename='waypoint')
router.register(r'groundobject', GroundObjectViewset, basename="groundobject")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('image/', CameraUploadAPIView.as_view(), name='upload-file')
]

urlpatterns += staticfiles_urlpatterns()
