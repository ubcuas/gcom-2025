from rest_framework import viewsets

from .models import GroundObject
from .models import Image
from .serializers import GroundObjectSerializer
from .serializers import ImageSerializer


# Create your views here.
class ImageViewset(viewsets.ModelViewSet):
    """Viewset for CRUD operations on Image"""

    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class GroundObjectViewset(viewsets.ModelViewSet):
    """Viewset for CRUD operations on GroundObjects"""

    queryset = GroundObject.objects.all()
    serializer_class = GroundObjectSerializer
