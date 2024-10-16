from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GroundObjectViewset
from .views import ImageViewset

router = DefaultRouter()
router.register(r"image", ImageViewset, basename="image")
router.register(r"groundobject", GroundObjectViewset, basename="groundobject")

urlpatterns = [
    path("", include(router.urls)),
]
