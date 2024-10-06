from rest_framework import viewsets
from .models import Route, Waypoint
from .serializers import RouteSerializer, OrderedWaypointSerializer


# Create your views here.
class OrderedWaypointViewset(viewsets.ModelViewSet):
    """Viewset for CRUD operations on Waypoints"""

    queryset = OrderedWaypoint.objects.all()
    serializer_class = OrderedWaypointSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(OrderedWaypointViewset, self).get_serializer(*args, **kwargs)


class RoutesViewset(viewsets.ModelViewSet):
    """Viewset for CRUD operations on Routes"""

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
