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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


from nav.views import RoutesViewset, OrderedWaypointViewset
from images.views import ImageViewset

router = DefaultRouter()

router.register(r"route", RoutesViewset, basename="route")
router.register(r"waypoint", OrderedWaypointViewset, basename="waypoint")
router.register(r"images", ImageViewset, basename="images")

urlpatterns = [
    # Swagger Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Admin Site
    path("admin/", admin.site.urls),
    # API
    path("api/", include(router.urls)),
    path("api/drone/", include("drone.urls")),
]

urlpatterns += staticfiles_urlpatterns()
