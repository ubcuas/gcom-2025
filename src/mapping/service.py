import math


def distance(p1x, p1y, p2x, p2y):
    return math.sqrt(math.pow(p1x - p2x, 2) + math.pow(p1y - p2y, 2))


def meshl(xcount, ycount, overlap):

    meshGrid = []

    for y in range(ycount):
        for x in range(xcount):
            meshGrid.append((x + overlap) / (xcount - (1 - 2 * overlap)))
    return meshGrid


def meshr(xcount, ycount, overlap):
    meshGrid = []

    for y in range(ycount):
        for x in range(xcount):
            meshGrid.append((math.floor(y) + overlap) / (ycount - (1 - 2 * overlap)))
    return meshGrid


# Function to convert lat/lon differences to meters relative to a reference point
def lat_lon_to_meters(coords):
    """
    Converts latitude and longitude to Cartesian coordinates in meters.
    Args:
        coords: List of tuples [(lat, lon), ...].
    Returns:
        List of tuples [(x, y), ...] where x and y are distances in meters.
    """
    # Earth's approximate conversion factors
    meters_per_degree_lat = 111320  # meters per degree latitude
    ref_lat, ref_lon = coords[0]  # Reference point (origin)
    ref_lat_rad = math.radians(ref_lat)  # Convert latitude to radians

    # Convert to meters relative to the reference point
    meter_coords = [
        (
            (lon - ref_lon)
            * meters_per_degree_lat
            * math.cos(ref_lat_rad),  # x: longitude adjusted by cosine
            (lat - ref_lat) * meters_per_degree_lat,  # y: latitude
        )
        for lat, lon in coords
    ]
    return meter_coords
