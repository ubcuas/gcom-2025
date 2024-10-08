from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import AreaOfInterestSerializer
from .models import AreaOfInterest
import json

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
