import json
import os
from django.http import FileResponse, HttpResponse, JsonResponse
import gzip


def serve_metadata(request):
    """
    Serves the mapbox gl metadata json file
    Also adds in the tile url pattern so that it points to the correct endpoint
    """
    metadata_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "metadata.json"
    )
    with open(metadata_path, "r") as f:
        metadata_json = json.load(f)
        metadata_json["tiles"] = [
            request.build_absolute_uri("tiles/") + "{z}/{x}/{y}.pbf"
        ]
        return JsonResponse(metadata_json)


def serve_style_json(request):
    """
    Serve the mapbox gl style json file
    This file specifies map style layers and also points to
    the metadata file url and the font glyph url pattern
    """
    style_json_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "osmbright.json"
    )
    with open(style_json_path, "r") as f:
        style_json = json.load(f)

        # Sets the metadata file url under "sources"
        style_json["sources"]["openmaptiles"]["url"] = request.build_absolute_uri(
            "metadata"
        )
        # We can't include "{}" characters in the url pattern because they will be serialized to %7B and %7D chars
        style_json["glyphs"] = (
            request.build_absolute_uri("fonts/") + "{fontstack}/{range}.pbf"
        )

        return JsonResponse(style_json)


def serve_glyphs(_, fontstack, fontrange):
    """
    Serves glyph files from the map_fonts directory
    These glyphs are just fonts encoded as vector .pbf files
    This makes them efficient to serve

    URL Pattern Example: /fonts/Noto%20Sans%20Regular/0-255.pbf
    """

    glyphs_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "map_fonts",
        fontstack,
        f"{fontrange}",
    )

    if not os.path.exists(glyphs_path):
        return JsonResponse({"message": "Font not found"}, status=404)

    try:
        response = FileResponse(
            open(glyphs_path, "rb"), content_type="application/x-protobuf"
        )
        return response
    except IOError:
        return JsonResponse({"message": "Error reading glyph file"}, status=500)


def serve_tiles(_, z, x, y):
    """
    Serves map tiles from the tile_data directory
    Each is a .pbf file that contains the tile as vector data
    For info about generating these tiles, see the README

    URL Pattern Example: /tiles/14/2620/6337.pbf
    where 14 is the zoom level, 2620 is the x coordinate, and 6337 is the y coordinate
    """

    tiles_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tile_data",
        str(z),
        str(x),
        f"{y}.pbf",
    )

    print("tiles_path", tiles_path)
    if not os.path.exists(tiles_path):
        response = FileResponse(b"", content_type="application/x-protobuf", status=204)
        return response

    try:
        with gzip.open(tiles_path, "rb") as f:
            tile_data = f.read()
        response = HttpResponse(
            content=tile_data,
            content_type="application/x-protobuf",
        )
        return response

    except IOError:
        return JsonResponse({"message": "Error reading tile file"}, status=500)
