from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to convert Image objects to JSON"""

    class Meta:
        model = Image
        fields = "__all__"
