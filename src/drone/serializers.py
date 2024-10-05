from drone.models import DroneTelemetry
from rest_framework import serializers


class DroneTelemetrySerializer(serializers.ModelSerializer):
    vertical_velocity = serializers.FloatField(source="vertical_speed")
    velocity = serializers.FloatField(source="speed")

    class Meta:
        model = DroneTelemetry
        fields = (
            "timestamp",
            "latitude",
            "longitude",
            "altitude",
            "vertical_velocity",
            "velocity",
            "heading",
            "battery_voltage",
        )
