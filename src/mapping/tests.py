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

    def test_post_n_get_area_of_interest(self):
        # test post
        test_object = {
            "area_of_interest": [
                {"latitude": 1, "longitude": 2, "altitude": 3},
                {"latitude": 4, "longitude": 5, "altitude": 6},
                {"latitude": 7, "longitude": 8, "altitude": 9},
                {"latitude": 10, "longitude": 11, "altitude": 12},
            ]
        }

        post_response = self.client.post(
            "/api/mapping/area_of_interest",
            json.dumps(test_object),
            content_type="application/json",
        )

        self.assertEqual(post_response.status_code, 200)

        # test get
        get_response = self.client.get(
            "/api/mapping/area_of_interest",
        )

        returned_object = json.loads(get_response.content)

        # test correct data is saved
        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(returned_object["area_of_interest"][0]["latitude"], 1)
        self.assertEqual(returned_object["area_of_interest"][0]["longitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][0]["altitude"], 3)
        self.assertEqual(returned_object["area_of_interest"][1]["latitude"], 4)
        self.assertEqual(returned_object["area_of_interest"][1]["longitude"], 5)
        self.assertEqual(returned_object["area_of_interest"][1]["altitude"], 6)
        self.assertEqual(returned_object["area_of_interest"][2]["latitude"], 7)
        self.assertEqual(returned_object["area_of_interest"][2]["longitude"], 8)
        self.assertEqual(returned_object["area_of_interest"][2]["altitude"], 9)
        self.assertEqual(returned_object["area_of_interest"][3]["latitude"], 10)
        self.assertEqual(returned_object["area_of_interest"][3]["longitude"], 11)
        self.assertEqual(returned_object["area_of_interest"][3]["altitude"], 12)

        # test overide
        test_object = {
            "area_of_interest": [
                {"latitude": 2, "longitude": 2},
                {"latitude": 2, "longitude": 2},
                {"latitude": 2, "longitude": 2},
                {"latitude": 2, "longitude": 2},
            ]
        }

        post_response = self.client.post(
            "/api/mapping/area_of_interest",
            json.dumps(test_object),
            content_type="application/json",
        )

        self.assertEqual(post_response.status_code, 200)

        # test get
        get_response = self.client.get(
            "/api/mapping/area_of_interest",
        )

        returned_object = json.loads(get_response.content)

        # test correct data is saved
        self.assertEqual(get_response.status_code, 200)

        self.assertEqual(returned_object["area_of_interest"][0]["latitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][0]["longitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][1]["latitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][1]["longitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][2]["latitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][2]["longitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][3]["latitude"], 2)
        self.assertEqual(returned_object["area_of_interest"][3]["longitude"], 2)
        self.assertFalse("altitude" in returned_object["area_of_interest"][0])
        self.assertFalse("altitude" in returned_object["area_of_interest"][1])
        self.assertFalse("altitude" in returned_object["area_of_interest"][2])
        self.assertFalse("altitude" in returned_object["area_of_interest"][3])
