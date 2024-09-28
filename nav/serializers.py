from rest_framework import serializers
from .models import Waypoint


class WaypointSerializer(serializers.ModelSerializer):
    """Serializer to convert Waypoint objects to JSON"""

    class Meta:
        model = Waypoint
        fields = "__all__"
