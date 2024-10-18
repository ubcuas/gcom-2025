import uuid
from django.db import models


class Route(models.Model):
    """Describes a route in GCOM

    Attributes:
        id: A unique identifier for the route
        name: The name of the route
    """

    name = models.CharField(max_length=32)


class Waypoint(models.Model):
    """Describes a position in GCOM

    Attributes:
        id: A unique identifier for the waypoint
        name: The name of the waypoint
        latitude: The latitude of the waypoint
        longitude: The longitude of the waypoint
        altitude: The altitude of the waypoint
    """

    # Vital Information
    id = models.UUIDField(
        primary_key=True, null=False, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=32)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    altitude = models.FloatField()

    # Enums
    class PassOptions(models.IntegerChoices):
        """Defines the ways in which the drone can pass through the waypoint

        Attributes:
            PASSTHROUGH: The drone will pass through the waypoint without
                changing its orientation
            ORBIT_CWISE: The drone will pass through the
                waypoint and orbit around it in a clockwise direction
            ORBIT_CCWISE: The drone will pass through the
                waypoint and orbit around it in a counter-clockwise direction
        """

        PASSTHROUGH = 0, "Passthrough"
        ORBIT_CWISE = 1, "Orbit Clockwise"
        ORBIT_CCWISE = -1, "Orbit Counter-Clockwise"

    radius = models.FloatField(default=5)
    pass_radius = models.FloatField(default=5)
    pass_option = models.IntegerField(
        default=PassOptions.PASSTHROUGH, choices=PassOptions
    )


class OrderedWaypoint(Waypoint):
    """Represents a Waypoint which has a specific ordering. Extends Waypoint

    Attributes:
        order: The order in which the waypoint should be visited
    """

    order = models.IntegerField(null=False)
    route = models.ForeignKey(Route, related_name="waypoints", on_delete=models.CASCADE)
