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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from images.views import ImageViewset
from rest_framework.routers import DefaultRouter

from nav.views import WaypointViewset

router = DefaultRouter()
router.register(r"waypoint", WaypointViewset, basename="waypoint")
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
    path("api/images/", include("images.urls")),
]

urlpatterns += staticfiles_urlpatterns()
