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
