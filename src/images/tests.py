from io import BytesIO
import json
from django.test import TestCase
from .models import Image
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PILImage
from django.test import override_settings
import shutil


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
