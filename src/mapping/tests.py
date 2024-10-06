from django.test import TestCase
from .serializers import AreaOfInterestSerializer
from rest_framework.test import APITestCase
import json


class AreaOfInterestValidationTest(TestCase):
    def setUp(self):
        pass

    def test_expected(self):

        # test for proper input
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), True)

        # test for missing a altitude
        # in case boundary points don't include altitude
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1},
                {"latitude": 1, "longitude": 1},
                {"latitude": 1, "longitude": 1},
                {"latitude": 1, "longitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), True)

    def test_missing_attribute(self):

        # test for missing area_of_interest
        test_object = {}
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), False)

        # test for null area_of_interest
        test_object = {"area_of_interest": None}
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), False)

        # test for missing a latitude
        test_object = {
            "area_of_interest": [
                {"longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        if valid_ser.is_valid():
            print(valid_ser.validated_data["area_of_interest"][0])
        self.assertEqual(valid_ser.is_valid(), False)

        # test for null altitude
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1, "altitude": None},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), False)

    def test_longer_list(self):
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), False)

    def test_shorter_list(self):
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }
        valid_ser = AreaOfInterestSerializer(data=test_object)
        self.assertEqual(valid_ser.is_valid(), False)


class AreaOfInterestEndpointTest(APITestCase):
    def setUp(self):
        pass

    def test_post_area_of_interest(self):
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
                {"latitude": 1, "longitude": 1, "altitude": 1},
            ]
        }

        response = self.client.post(
            "/api/mapping/area_of_interest",
            json.dumps(test_object),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
