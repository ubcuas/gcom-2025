from rest_framework import viewsets
from .models import Route, OrderedWaypoint
from .serializers import RouteSerializer, OrderedWaypointSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


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

    queryset = Route.objects.all().prefetch_related("waypoints")
    serializer_class = RouteSerializer

    @action(detail=True, methods=["post"], url_path="reorder-waypoints")
    def reorder_waypoints(self, request, pk=None):
        """
        Action to reorder waypoints in a route
        Args:
            request: The request object - contains the reordered waypoint ids
            pk: The primary key of the route whose waypoints we're reordering
        """
        route = self.get_object()

        waypoints = OrderedWaypoint.objects.filter(route=route)

        if (
            not request.data
            or not isinstance(request.data, list)
            or len(request.data) != len(waypoints)
        ):
            return Response(
                {"error": "Please provide a list of all waypoint IDs"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reordered_waypoint_ids = request.data
        for idx, waypoint_id in enumerate(reordered_waypoint_ids):
            try:
                waypoint = waypoints.get(id=waypoint_id)
                waypoint.order = idx
                waypoint.save()
            except OrderedWaypoint.DoesNotExist:
                return Response(
                    {"error": f"Waypoint with  not found with id: {waypoint_id}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"success": "Waypoints reordered successfully"}, status=status.HTTP_200_OK
        )
