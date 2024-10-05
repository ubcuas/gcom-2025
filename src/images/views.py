from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    serializer_class = GroundObject


# CreateGroundObject
@api_view(["POST"])
def create_ground_object(request):
    serializer = GroundObjectSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data.get("id") != -1:
            return Response(
                {"message": "Non-sentinel ID passed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(id=0)  # Replace sentinel ID with 0 (auto increment)
        return Response(
            {"message": "GroundObject created!", "model": serializer.data},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "Invalid object data", "data": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# CreateGroundObjectBatch
@api_view(["POST"])
def create_ground_object_batch(request):
    serializer = GroundObjectSerializer(data=request.data, many=True)
    if serializer.is_valid():
        for obj in serializer.validated_data:
            if obj.get("id") != -1:
                return Response(
                    {"message": f"Non-sentinel ID passed for object {obj}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        serializer.save(id=0)  # Replace sentinel ID with 0 for all objects
        return Response(
            {"message": "GroundObjects created!", "models": serializer.data},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "Invalid objects data", "data": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# EditGroundObject
@api_view(["PATCH"])
def edit_ground_object(request, id):
    ground_object = get_object_or_404(GroundObject, id=id)
    data = request.data.copy()
    if "id" in data and data["id"] != 0:
        return Response(
            {"message": "ID is not editable"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = GroundObjectSerializer(ground_object, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"message": "GroundObject updated!", "model": serializer.data},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "Invalid object data", "data": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# GetGroundObject
@api_view(["GET"])
def get_ground_object(request, id):
    ground_object = get_object_or_404(GroundObject, id=id)
    serializer = GroundObjectSerializer(ground_object)
    return Response(
        {"message": "Object found!", "model": serializer.data},
        status=status.HTTP_200_OK,
    )


# DeleteGroundObject
@api_view(["DELETE"])
def delete_ground_object(request, id):
    ground_object = get_object_or_404(GroundObject, id=id)
    ground_object.delete()
    return Response(
        {"message": "GroundObject deleted!", "model": {}}, status=status.HTTP_200_OK
    )


# DeleteGroundObjectBatch
@api_view(["DELETE"])
def delete_ground_object_batch(request):
    ids = request.data.get("ids", [])
    for id in ids:
        if id < 0:
            return Response(
                {"message": f"Invalid ID; Negative ID entered for {id}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        ground_object = GroundObject.objects.filter(id=id).first()
        if not ground_object:
            return Response(
                {"message": f"Requested object {id} does not exist!"},
                status=status.HTTP_404_NOT_FOUND,
            )
        ground_object.delete()
    return Response(
        {"message": "GroundObjects deleted!", "model": {}}, status=status.HTTP_200_OK
    )


# GetAllGroundObjects
@api_view(["GET"])
def get_all_ground_objects(request):
    objects = GroundObject.objects.all()
    serializer = GroundObjectSerializer(objects, many=True)
    return Response(
        {"message": "GroundObjects found!", "models": serializer.data},
        status=status.HTTP_200_OK,
    )
