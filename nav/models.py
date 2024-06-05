import uuid
from django.db import models
from mission.models import Mission

class Waypoint(models.Model):
    
    # Vital Information
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    altitude = models.FloatField()

    # Enums
    class PassOptions(models.IntegerChoices):
        PASSTHROUGH = 0, "Passthrough"
        ORBIT_CWISE = 1, "Orbit Clockwise"
        ORBIT_CCWISE = -1, "Orbit Counter-Clockwise"

    radius = models.FloatField(default=5)
    pass_radius = models.FloatField(default=5)
    pass_option = models.IntegerField(default=PassOptions.PASSTHROUGH, choices=PassOptions)
    
class OrderedWaypoint(Waypoint):
    order = models.IntegerField(null=False)

class MissionWaypoint(OrderedWaypoint):
    mission = models.ForeignKey(Mission, on_delete=models.CASCADE)