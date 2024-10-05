from django.urls import path

from .views import create_ground_object
from .views import create_ground_object_batch
from .views import delete_ground_object
from .views import delete_ground_object_batch
from .views import edit_ground_object
from .views import get_all_ground_objects
from .views import get_ground_object

urlpatterns = [
    path("groundobject/", create_ground_object, name="create_ground_object"),
    path(
        "groundobjects/", create_ground_object_batch, name="create_ground_object_batch"
    ),
    path("groundobject/<int:id>/", edit_ground_object, name="edit_ground_object"),
    path("groundobject/<int:id>/", get_ground_object, name="get_ground_object"),
    path("groundobject/<int:id>/", delete_ground_object, name="delete_ground_object"),
    path(
        "groundobjects/delete/",
        delete_ground_object_batch,
        name="delete_ground_object_batch",
    ),
    path("groundobjects/", get_all_ground_objects, name="get_all_ground_objects"),
]
