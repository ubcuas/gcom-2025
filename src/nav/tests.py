from django.test import TestCase
from .models import Waypoint
from rest_framework.test import APITestCase

class WaypointModelTest(TestCase):
    def setUp(self):
        Waypoint.objects.create(
            name="Test Waypoint",
            latitude=0,
            longitude=0,
            altitude=0
        )

    def test_waypoint(self):
        waypoint = Waypoint.objects.get(name="Test Waypoint")
        self.assertEqual(waypoint.name, "Test Waypoint")
        self.assertEqual(waypoint.latitude, 0)
        self.assertEqual(waypoint.longitude, 0)
        self.assertEqual(waypoint.altitude, 0)

    def test_cannot_create_without_name(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name=None,
                latitude=0,
                longitude=0,
                altitude=0
            )

    def test_cannot_create_without_latitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint",
                latitude=None,
                longitude=0,
                altitude=0
            )

    def test_cannot_create_without_longitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint",
                latitude=0,
                longitude=None,
                altitude=0
            )

    def test_cannot_create_without_altitude(self):
        with self.assertRaises(Exception):
            Waypoint.objects.create(
                name="Test Waypoint",
                latitude=0,
                longitude=0,
                altitude=None
            )

class WaypointEndpointTests(APITestCase):
    def setUp(self):
        Waypoint.objects.create(
            name="Test Waypoint",
            latitude=0,
            longitude=0,
            altitude=0
        )

    def test_get_waypoint(self):
        response = self.client.get("/api/waypoint/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Waypoint")

    def test_create_waypoint(self):
        response = self.client.post("/api/waypoint/", {
            "name": "Test Waypoint 2",
            "latitude": 0,
            "longitude": 0,
            "altitude": 0
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Waypoint.objects.count(), 2)
        self.assertEqual(Waypoint.objects.get(name="Test Waypoint 2").name, "Test Waypoint 2")

    def test_update_waypoint(self):
        uuid = Waypoint.objects.get(name="Test Waypoint").id
        response = self.client.put(f"/api/waypoint/{uuid}/", {
            "name": "Updated Waypoint",
            "latitude": 0,
            "longitude": 0,
            "altitude": 0
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Waypoint.objects.get(id=uuid).name, "Updated Waypoint")

    def test_delete_waypoint(self):
        uuid = Waypoint.objects.get(name="Test Waypoint").id
        response = self.client.delete(f"/api/waypoint/{uuid}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Waypoint.objects.count(), 0)