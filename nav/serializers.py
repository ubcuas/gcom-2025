from rest_framework import serializers
from .models import Waypoint

class WaypointSerializer(serializers.ModelSerializer):
    mission = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    
    class Meta:
        model = Waypoint
        fields = '__all__'