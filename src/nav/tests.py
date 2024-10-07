import json
from django.test import TestCase
from .models import OrderedWaypoint, Route, Waypoint
from rest_framework.test import APITestCase


class WaypointModelTest(TestCase):
    def setUp(self):
        Waypoint.objects.create(
            name="Test Waypoint", latitude=0, longitude=0, altitude=0
        )

    def test_waypoint(self):
        waypoint = Waypoint.objects.get(name="Test Waypoint")
        self.assertEqual(waypoint.name, "Test Waypoint")
        self.assertEqual(waypoint.latitude, 0)
        self.assertEqual(waypoint.longitude, 0)
        self.assertEqual(waypoint.altitude, 0)

    def test_cannot_create_without_name(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(name=None, latitude=0, longitude=0, altitude=0)

    def test_cannot_create_without_latitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint", latitude=None, longitude=0, altitude=0
            )

    def test_cannot_create_without_longitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint", latitude=0, longitude=None, altitude=0
            )

    def test_cannot_create_without_altitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint", latitude=0, longitude=0, altitude=None
            )


class WaypointEndpointTests(APITestCase):
    def setUp(self):
        test_route = Route.objects.create(name="Test Route")
        self.test_route_id = test_route.id

        OrderedWaypoint.objects.create(
            name="Test Waypoint",
            latitude=0,
            longitude=0,
            altitude=0,
            order=0,
            route=test_route,
        )

    def test_get_waypoint(self):
        response = self.client.get("/api/waypoint/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Waypoint")

    def test_create_waypoint(self):
        response = self.client.post(
            "/api/waypoint/",
            {
                "name": "Test Waypoint 2",
                "latitude": 0,
                "longitude": 0,
                "altitude": 0,
                "route": self.test_route_id,
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Waypoint.objects.count(), 2)
        self.assertEqual(
            Waypoint.objects.get(name="Test Waypoint 2").name, "Test Waypoint 2"
        )

    def test_update_waypoint(self):
        uuid = OrderedWaypoint.objects.get(name="Test Waypoint").id
        response = self.client.put(
            f"/api/waypoint/{uuid}/",
            {
                "name": "Updated Waypoint",
                "latitude": 0,
                "longitude": 0,
                "altitude": 0,
                "route": self.test_route_id,
                "order": 1,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Waypoint.objects.get(id=uuid).name, "Updated Waypoint")

    def test_delete_waypoint(self):
        uuid = Waypoint.objects.get(name="Test Waypoint").id
        response = self.client.delete(f"/api/waypoint/{uuid}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Waypoint.objects.count(), 0)


class RouteModelTest(TestCase):
    def setUp(self):
        Route.objects.create(name="Test Route")

    def test_route(self):
        route = Route.objects.get(name="Test Route")
        self.assertEqual(route.name, "Test Route")

    def test_cannot_create_without_name(self):
        with self.assertRaises(Exception):
            Route.objects.create(name=None)


class RouteEndpointTests(APITestCase):
    def setUp(self):
        Route.objects.create(name="Test Route")

    def test_get_route(self):
        response = self.client.get("/api/route/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Route")

    def test_create_route(self):
        response = self.client.post("/api/route/", {"name": "Test Route 2"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Route.objects.count(), 2)
        self.assertEqual(Route.objects.get(name="Test Route 2").name, "Test Route 2")

    def test_update_route(self):
        uuid = Route.objects.get(name="Test Route").id
        response = self.client.put(f"/api/route/{uuid}/", {"name": "Updated Route"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Route.objects.get(id=uuid).name, "Updated Route")

    def test_delete_route(self):
        uuid = Route.objects.get(name="Test Route").id
        response = self.client.delete(f"/api/route/{uuid}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Route.objects.count(), 0)

    def test_reorder_waypoints(self):
        route = Route.objects.get(name="Test Route")
        OrderedWaypoint.objects.create(
            name="Test Waypoint 1",
            latitude=0,
            longitude=0,
            altitude=0,
            order=1,
            route=route,
        )
        OrderedWaypoint.objects.create(
            name="Test Waypoint 2",
            latitude=0,
            longitude=0,
            altitude=0,
            order=1,
            route=route,
        )

        OrderedWaypoint.objects.create(
            name="Test Waypoint 3",
            latitude=0,
            longitude=0,
            altitude=0,
            order=1,
            route=route,
        )

        response = self.client.post(
            f"/api/route/{route.id}/reorder-waypoints/",
            content_type="application/json",
            data=json.dumps(
                [
                    str(OrderedWaypoint.objects.get(name="Test Waypoint 2").id),
                    str(OrderedWaypoint.objects.get(name="Test Waypoint 3").id),
                    str(OrderedWaypoint.objects.get(name="Test Waypoint 1").id),
                ]
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(OrderedWaypoint.objects.get(name="Test Waypoint 2").order, 0)
        self.assertEqual(OrderedWaypoint.objects.get(name="Test Waypoint 3").order, 1)
        self.assertEqual(OrderedWaypoint.objects.get(name="Test Waypoint 1").order, 2)
