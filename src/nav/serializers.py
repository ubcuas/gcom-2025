from rest_framework import serializers
from .models import OrderedWaypoint, Route


class OrderedWaypointSerializer(serializers.ModelSerializer):
    """Serializer to convert Waypoint objects to JSON"""

    class Meta:
        model = OrderedWaypoint
        ordering = ["order"]
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    """Serializer to convert Route objects to JSON"""

    waypoints = OrderedWaypointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ["id", "name", "waypoints"]
