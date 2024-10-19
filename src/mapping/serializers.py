from rest_framework import serializers


class BoundaryPointSerializer(serializers.Serializer):
    """stores the structure of boundary point for verification"""

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
    altitude = serializers.FloatField(required=False)


class AreaOfInterestSerializer(serializers.Serializer):
    """stores the structure of area of interest for verification"""

    area_of_interest = serializers.ListField(
        child=BoundaryPointSerializer(), required=True, min_length=4, max_length=4
    )
