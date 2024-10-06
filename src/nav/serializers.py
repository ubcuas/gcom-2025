from rest_framework import serializers
from .models import OrderedWaypoint, Route


class OrderedWaypointSerializer(serializers.ModelSerializer):
    """Serializer to convert Waypoint objects to JSON"""

    class Meta:
        model = OrderedWaypoint
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    """Serializer to convert Route objects to JSON"""

    class Meta:
        model = Route
        fields = "__all__"
