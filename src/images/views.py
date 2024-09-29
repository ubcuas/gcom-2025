from django.shortcuts import render
from .models import Image
from .serializers import ImageSerializer
from rest_framework import viewsets

# Create your views here.
class ImageViewset(viewsets.ModelViewSet):
    """Viewset for CRUD operations on Image"""

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    