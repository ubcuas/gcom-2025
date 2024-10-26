from django.http import JsonResponse
from django.urls import path
from .views import serve_glyphs, serve_metadata, serve_style_json, serve_tiles

urlpatterns = [
    path("osmbright", serve_style_json, name="osmbright"),
    path("fonts/<str:fontstack>/<str:fontrange>", serve_glyphs, name="fonts"),
    path("tiles/<int:z>/<int:x>/<int:y>.pbf", serve_tiles, name="tiles"),
    path("metadata", serve_metadata, name="metadata"),
]
