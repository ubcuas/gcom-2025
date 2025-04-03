from django.urls import path
from . import views

urlpatterns = [
    path(
        "area_of_interest",
        views.process_area_of_interest,
        name="process_area_of_interest",
    ),
    path(
        "points_on_route",
        views.process_points_on_route,
        name="process_points_on_route",
    ),
]
