from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .serializers import AreaOfInterestSerializer
import json


@csrf_exempt
@require_http_methods(["POST"])
def post_area_of_interest(request):

    try:
        valid_ser = AreaOfInterestSerializer(data=json.loads(request.body))
        if not valid_ser.is_valid():
            return JsonResponse({"error": "Invalid input"}, status=400)

        return HttpResponse("yes", status=200)
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid input"}, status=400)


# @require_http_methods(["GET"])
# def get_area_of_interest(request):
#     try:
#         return JsonResponse({"error": "not implemented"}, status=400)
#     except (KeyError, ValueError, TypeError):
#         return JsonResponse({"error": "Invalid input"}, status=400)
