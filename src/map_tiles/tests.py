from unittest.mock import MagicMock, patch
from django.test import TestCase, Client
from django.urls import reverse
import os
import json


class MapTilesViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def test_serve_metadata(self):
        response = self.client.get(reverse("metadata"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()

        metadata_path = os.path.join(self.base_dir, "metadata.json")
        with open(metadata_path, "r") as f:
            expected_metadata = json.load(f)

        expected_metadata["tiles"] = [
            response.wsgi_request.build_absolute_uri("tiles/") + "{z}/{x}/{y}.pbf"
        ]

        self.assertEqual(data, expected_metadata)

    def test_serve_style_json(self):
        response = self.client.get(reverse("osmbright"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")

        data = response.json()

        # Load the expected osmbright.json
        style_json_path = os.path.join(self.base_dir, "osmbright.json")
        with open(style_json_path, "r") as f:
            expected_style = json.load(f)

        # Modify the expected style JSON as per the view logic
        expected_style["sources"]["openmaptiles"]["url"] = (
            response.wsgi_request.build_absolute_uri("metadata")
        )
        expected_style["glyphs"] = (
            response.wsgi_request.build_absolute_uri("fonts/")
            + "{fontstack}/{range}.pbf"
        )

        self.assertEqual(data, expected_style)

    def test_serve_glyphs_file_exists(self):
        # Test with an existing glyph file
        fontstack = "Noto Sans Regular"
        fontrange = "0-255.pbf"

        url = reverse("fonts", args=[fontstack, fontrange])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/x-protobuf")

        # Read the expected glyph file
        glyphs_path = os.path.join(self.base_dir, "map_fonts", fontstack, fontrange)
        with open(glyphs_path, "rb") as f:
            expected_content = f.read()

        # Since FileResponse uses streaming_content, we need to get the content
        content = b"".join(response.streaming_content)
        self.assertEqual(content, expected_content)

    def test_serve_glyphs_file_not_exists(self):
        # Test with a non-existing glyph file
        fontstack = "NonexistentFont"
        fontrange = "0-255.pbf"

        url = reverse("fonts", args=[fontstack, fontrange])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(data["message"], "Font not found")

    def test_serve_tiles_file_not_exists(self):
        # Test with a non-existing tile file
        z = 14
        x = 9999  # Assuming this tile does not exist
        y = 9999
        url = reverse("tiles", args=[z, x, y])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response["Content-Type"], "application/x-protobuf")

        # Since FileResponse uses streaming_content, we need to get the content
        content = b"".join(response.streaming_content)
        self.assertEqual(content, b"")

    def test_serve_tiles_file_exists(self):
        z = 14
        x = 1905
        y = 4301
        url = reverse("tiles", args=[z, x, y])

        # Mock tile data
        tile_data = b"test tile data"

        def mock_gzip_open(file, mode="rb", *args, **kwargs):
            # Create a mock file object
            mock_file = MagicMock()
            mock_file.__enter__.return_value = mock_file
            mock_file.__exit__.return_value = False
            # Set the read method to return the tile_data
            mock_file.read.return_value = tile_data
            return mock_file

        with patch("os.path.exists") as mock_exists, patch("gzip.open", mock_gzip_open):
            # Simulate that the file exists
            mock_exists.return_value = True

            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response["Content-Type"], "application/x-protobuf")
            self.assertEqual(response.content, tile_data)
