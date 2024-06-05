from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import GroundObject
from .serializers import GroundObjectSerializer, CameraImageSerializer


# Create your views here.
class GroundObjectViewset(viewsets.ModelViewSet):
    queryset = GroundObject.objects.all()
    serializer_class = GroundObjectSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(GroundObjectViewset, self).get_serializer(*args, **kwargs)
    
class CameraUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = CameraImageSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
