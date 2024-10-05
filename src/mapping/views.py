from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .serializers import AreaOfInterestSerializer


@require_http_methods(["POST"])
def post_area_of_interest(request):

    try:
        valid_ser = AreaOfInterestSerializer(data=request.body)
        if not valid_ser.is_valid():
            return JsonResponse({"error": valid_ser.errors}, status=400)

        return HttpResponse(status=200)
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "Invalid input"}, status=400)


# @require_http_methods(["GET"])
# def get_area_of_interest(request):
#     try:
#         return JsonResponse({"error": "not implemented"}, status=400)
#     except (KeyError, ValueError, TypeError):
#         return JsonResponse({"error": "Invalid input"}, status=400)
