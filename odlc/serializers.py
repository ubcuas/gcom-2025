from rest_framework import serializers
from .models import GroundObject, CameraImage

class GroundObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroundObject
        fields = '__all__'

class CameraImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraImage
        fields = '__all__'