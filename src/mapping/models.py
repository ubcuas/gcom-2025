from django.db import models

# pylint: disable=no-member


class AreaOfInterest(models.Model):
    # stores list of points as a json field as this seem to be the cleanest way to do so
    area_of_interest = models.JSONField()

    def save(self, **kwargs):
        # make sure only one is present by deleting old entry
        if AreaOfInterest.objects.count() != 0:
            AreaOfInterest.objects.all().delete()
        super().save(**kwargs)  # Call the "real" save() method.


class MappingRoute(models.Model):
    """Singleton Model for drone route for mapping"""
    # fields
    # Stored list of points as arbitrary length JSON field to be consistent with area of interest
    # altitude is how high the drone needs to be from ground when taking these pictures.
    points_on_route = models.JSONField()
    altitude = models.FloatField()

    # methods
    def save(self, **kwargs):

        if MappingRoute.objects.count() != 0:
            MappingRoute.objects.all().delete()
        super().save(**kwargs)
