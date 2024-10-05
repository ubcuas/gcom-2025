from django.urls import path
from . import views

urlpatterns = [
    path("mapping/area_of_interest", views.post_area_of_interest, name="post_area_of_interest"),
    # path("mapping/area_of_interest", views.get_area_of_interest, name="get_area_of_interest"),
]
