from django.test import TestCase
from .models import Waypoint

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