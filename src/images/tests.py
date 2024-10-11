import json
import shutil
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError
from django.test import override_settings
from django.test import TestCase
from PIL import Image as PILImage
from rest_framework import status
from rest_framework.test import APITestCase
from .models import GroundObject
from .models import Image

TEST_DIR = "test_files"


# Create your tests here.
class ImageModelTests(TestCase):
    def setUp(self):
        Image.objects.create(
            image="images/test.jpg",
            title="Test Image",
            image_type="visible",
            taken_at="2021-01-01 12:00:00",
        )

    def test_image(self):
        image = Image.objects.get(title="Test Image")
        self.assertEqual(image.title, "Test Image")
        self.assertEqual(image.image_type, "visible")
        self.assertEqual(
            image.taken_at.strftime("%Y-%m-%d %H:%M:%S"), "2021-01-01 12:00:00"
        )

    def test_representation(self):
        image = Image.objects.get(title="Test Image")
        self.assertEqual(str(image), "2021-01-01 12:00:00")

    def test_cannot_create_without_date(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(
                image="images/test.jpg", title="Test Image", image_type="visible"
            )

    def test_cannot_create_without_title(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(
                image="images/test.jpg",
                title=None,
                image_type="visible",
                taken_at="2021-01-01 12:00:00",
            )

    def test_cannot_create_without_image_type(self):
        with self.assertRaises(IntegrityError):
            Image.objects.create(
                image="images/test.jpg",
                title="Test Image",
                taken_at="2021-01-01 12:00:00",
                image_type=None,
            )


@override_settings(MEDIA_ROOT=TEST_DIR)
class ImageEndpointTests(APITestCase):
    @staticmethod
    def generate_image_file(color="red", size=(100, 100), format="JPEG"):
        """
        Generates an image in memory and returns it as a SimpleUploadedFile object.
        """
        image = PILImage.new("RGB", size, color=color)
        byte_io = BytesIO()
        image.save(byte_io, format=format)
        byte_io.seek(0)
        return SimpleUploadedFile(
            "test_image.jpg", byte_io.getvalue(), content_type="image/jpeg"
        )

    def setUp(self):
        with self.generate_image_file() as test_image:
            Image.objects.create(
                image=test_image,
                title="Test Image",
                image_type="visible",
                taken_at="2021-01-01 12:00:00",
            )

    def test_get_images(self):
        response = self.client.get("/api/images/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Test Image")
        self.assertEqual(response.data[0]["image_type"], "visible")
        self.assertEqual(response.data[0]["taken_at"], "2021-01-01T12:00:00Z")

    def test_post_image(self):
        image_count = Image.objects.count()
        with self.generate_image_file() as test_image:
            response = self.client.post(
                "/api/images/",
                {
                    "image": test_image,
                    "title": "New Image",
                    "image_type": "thermal",
                    "taken_at": "2021-01-01 12:00:00",
                },
                format="multipart",
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Image.objects.count(), image_count + 1)

        image_id = json.loads(response.content)["id"]
        new_image = Image.objects.get(id=image_id)
        self.assertEqual(new_image.title, "New Image")
        self.assertEqual(new_image.image_type, "thermal")
        self.assertEqual(
            new_image.taken_at.strftime("%Y-%m-%d %H:%M:%S"), "2021-01-01 12:00:00"
        )

    def test_post_image_invalid_request(self):
        image_count = Image.objects.count()
        with self.generate_image_file() as test_image:
            response = self.client.post(
                "/api/images/",
                {"image": test_image, "title": "New Image", "image_type": "thermal"},
                format="multipart",
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Image.objects.count(), image_count)

    def test_post_image_file_invalid(self):
        image_count = Image.objects.count()
        response = self.client.post(
            "/api/images/",
            {
                "image": b"invalid.jpg",
                "title": "New Image",
                "image_type": "thermal",
                "taken_at": "2021-01-01 12:00:00",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Image.objects.count(), image_count)

    def test_get_image(self):
        response = self.client.get("/api/images/1/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Image")
        self.assertEqual(response.data["image_type"], "visible")
        self.assertEqual(response.data["taken_at"], "2021-01-01T12:00:00Z")

    def test_get_all_images(self):
        response = self.client.get("/api/images/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Test Image")
        self.assertEqual(response.data[0]["image_type"], "visible")
        self.assertEqual(response.data[0]["taken_at"], "2021-01-01T12:00:00Z")

    def test_delete_image(self):
        image_count = Image.objects.count()
        with self.generate_image_file() as test_image:
            img = Image.objects.create(
                image=test_image,
                title="Test Image",
                image_type="visible",
                taken_at="2021-01-01 12:00:00",
            )
        response = self.client.delete(f"/api/images/{img.id}/", format="json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Image.objects.count(), image_count)

    def test_edit_image(self):
        with self.generate_image_file() as test_image:
            img = Image.objects.create(
                image=test_image,
                title="Test Image",
                image_type="visible",
                taken_at="2021-01-01 12:00:00",
            )

        response = self.client.patch(
            f"/api/images/{img.id}/",
            {
                "title": "New Image",
                "image_type": "thermal",
                "taken_at": "2021-01-01 12:00:00",
            },
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        updated_image = Image.objects.get(id=img.id)
        self.assertEqual(updated_image.title, "New Image")
        self.assertEqual(updated_image.image_type, "thermal")
        self.assertEqual(
            updated_image.taken_at.strftime("%Y-%m-%d %H:%M:%S"), "2021-01-01 12:00:00"
        )

    def tearDown(self):
        shutil.rmtree(TEST_DIR)


class GroundObjectModelTests(TestCase):
    def setUp(self):
        GroundObject.objects.create(
            object_type=GroundObject.ObjectType.STANDARD,
            lat=12.3456,
            long=78.9101,
            shape=GroundObject.Shape.CIRCLE,
            color=GroundObject.Color.RED,
            text="Sample Text",
            text_color=GroundObject.Color.BLACK,
        )

    def test_ground_object_creation(self):
        ground_object = GroundObject.objects.get(text="Sample Text")
        self.assertEqual(ground_object.object_type, GroundObject.ObjectType.STANDARD)
        self.assertEqual(ground_object.lat, 12.3456)
        self.assertEqual(ground_object.long, 78.9101)
        self.assertEqual(ground_object.shape, GroundObject.Shape.CIRCLE)
        self.assertEqual(ground_object.color, GroundObject.Color.RED)
        self.assertEqual(ground_object.text, "Sample Text")
        self.assertEqual(ground_object.text_color, GroundObject.Color.BLACK)

    def test_cannot_create_without_lat_long(self):
        with self.assertRaises(IntegrityError):
            GroundObject.objects.create(
                object_type=GroundObject.ObjectType.STANDARD,
                shape=GroundObject.Shape.CIRCLE,
                color=GroundObject.Color.RED,
                text="Sample Text",
                text_color=GroundObject.Color.BLACK,
            )

    def test_representation(self):
        ground_object = GroundObject.objects.get(text="Sample Text")
        self.assertEqual(str(ground_object), "Sample Text")


class GroundObjectEndpointTests(APITestCase):
    def setUp(self):
        self.ground_object = GroundObject.objects.create(
            object_type=GroundObject.ObjectType.STANDARD,
            lat=12.3456,
            long=78.9101,
            shape=GroundObject.Shape.CIRCLE,
            color=GroundObject.Color.RED,
            text="Sample Text",
            text_color=GroundObject.Color.BLACK,
        )

    def test_get_ground_object(self):
        response = self.client.get(
            f"/api/groundobject/{self.ground_object.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Sample Text")
        self.assertEqual(response.data["lat"], 12.3456)
        self.assertEqual(response.data["long"], 78.9101)

    def test_get_all_ground_objects(self):
        response = self.client.get("/api/groundobject/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["text"], "Sample Text")

    def test_create_ground_object(self):
        ground_object_count = GroundObject.objects.count()
        response = self.client.post(
            "/api/groundobject/",
            {
                "object_type": GroundObject.ObjectType.STANDARD,
                "lat": 10.1234,
                "long": 20.5678,
                "shape": GroundObject.Shape.RECTANGLE,
                "color": GroundObject.Color.BLUE,
                "text": "Sample Text",
                "text_color": GroundObject.Color.RED,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GroundObject.objects.count(), ground_object_count + 1)

    def test_delete_ground_object(self):
        response = self.client.delete(
            f"/api/groundobject/{self.ground_object.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(GroundObject.objects.count(), 0)

    def test_edit_ground_object(self):
        response = self.client.patch(
            f"/api/groundobject/{self.ground_object.id}/",
            {
                "text": "Updated Text",
                "color": GroundObject.Color.GREEN,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_object = GroundObject.objects.get(id=self.ground_object.id)
        self.assertEqual(updated_object.text, "Updated Text")
        self.assertEqual(updated_object.color, GroundObject.Color.GREEN)

    def test_create_ground_object_invalid_request(self):
        ground_object_count = GroundObject.objects.count()
        response = self.client.post(
            "/api/groundobject/",
            {
                "object_type": GroundObject.ObjectType.STANDARD,
                "shape": GroundObject.Shape.RECTANGLE,
                "color": GroundObject.Color.BLUE,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(GroundObject.objects.count(), ground_object_count)
