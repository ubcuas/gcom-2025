from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import AreaOfInterestSerializer
from .models import AreaOfInterest
from .models import MappingRoute
from .service import distance
from .service import meshl
from .service import meshr
import json
import math

# pylint: disable=no-member


@csrf_exempt
def process_area_of_interest(request):
    try:
        if request.method == "POST":
            valid_ser = AreaOfInterestSerializer(data=json.loads(request.body))

            if not valid_ser.is_valid():
                return HttpResponse("Invalid Input", status=400)

            a = str(valid_ser.validated_data["area_of_interest"])
            area_modelled = AreaOfInterest(
                area_of_interest=json.dumps(
                    valid_ser.validated_data["area_of_interest"]
                )
            )
            area_modelled.save()

            return HttpResponse(
                "Area of Interest Successfully Saved" + "\n" + a, status=200
            )
        elif request.method == "GET":
            area_modelled = AreaOfInterest.objects.last()
            if area_modelled is None:
                return HttpResponse("No Area Of Interest Saved", status=204)

            area = {"area_of_interest": json.loads(area_modelled.area_of_interest)}

            return JsonResponse(area, status=200)
        else:
            return HttpResponse("Correct Address, Incorrect Method", status=405)
    except (KeyError, ValueError, TypeError) as e:
        return HttpResponse("Server Error\n" + str(e), status=500)


@csrf_exempt
def process_points_on_route(request):
    # Uses 4 most recent boundary points to make route mapping
    try:
        if request.method == "POST":
            # Gets most recent Boundary points for computation
            area_modelled = AreaOfInterest.objects.last()
            if area_modelled is None:
                return HttpResponse("No Area Of Interest Saved", status=204)
            else:
                # Camera Parameters (Focal length, Sensor Width, Sensor Height, Image Width
                # Image Height, Ground Sample Distance, Image overlap %)
                d_focal, sw, iw, ih, gsd, o = (
                    0.012,
                    0.0131328,
                    3840,
                    2160,
                    0.025,
                    0.317,
                )

                width, height = gsd * iw, gsd * ih
                # Generating List of Points
                area = area_modelled.area_of_interest
                p1, p2, p3, p4 = area[0], area[1], area[2], area[3]
                p1x = p1["latitude"]
                p1y = p1["longidute"]
                p2x = p2["latitude"]
                p2y = p2["longidute"]
                p3x = p3["latitude"]
                p3y = p3["longidute"]
                p4x = p4["latitude"]
                p4y = p4["longidute"]
                # required altitude (meters)
                alt = (iw * d_focal * gsd) / sw

                # Maximum X and Y distances
                ylen1 = distance(p1x, p1y, p2x, p2y)
                ylen2 = distance(p3x, p3y, p4x, p4y)
                ymax = max(ylen1, ylen2)

                xlen1 = distance(p1x, p1y, p4x, p4y)
                xlen2 = distance(p2x, p2y, p3x, p3y)
                xmax = max(xlen1, xlen2)

                # Num pictures needed on X-axis and Y-axis
                xcount = math.ceil((xmax - (o * width)) / ((1 - o) * width)) + 1
                ycount = math.ceil((ymax - (o * height)) / ((1 - o) * height)) + 1

                # Creating Mesh Grids
                gridl = meshl(xcount, ycount, o)
                gridr = meshr(xcount, ycount, o)

                # Projecting Mesh Grid onto images
                final_grid = []
                for i in range(xcount * ycount):
                    newx = (p3x + gridl[i] * (p2x - p3x)) + gridr[i] * (
                        p4x - p3x + gridl[i] * (p1x - p2x + p3x - p4x)
                    )
                    newy = (p3y + gridl[i] * (p2y - p3y)) + gridr[i] * (
                        p4y - p3y + gridl[i] * (p1y - p2y + p3y - p4y)
                    )
                    final_grid.append([newx, newy])

                points = MappingRoute(
                    points_on_route=json.dumps(final_grid), altitude=json.dumps(alt)
                )
                points.save()

                return HttpResponse(
                    "New Mapping Route Successfully Saved" + "\n" + points, status=200
                )

        elif request.method == "GET":
            # Getting most recent drone rout from MappingRoute
            route = MappingRoute.objects.last()
            if route is None:
                return HttpResponse("No Drone Route Saved", status=204)

            points = {
                "points_on_route": json.loads(route.points_on_route),
                "altitude": json.loads(route.altitude),
            }

            return JsonResponse(points, status=200)

        else:
            return HttpResponse("Correct Address, Incorrect Method", status=405)
    except (KeyError, ValueError, TypeError) as e:
        return HttpResponse("Server Error\n" + str(e), status=500)
