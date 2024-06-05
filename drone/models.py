from django.db import models
from django.utils.translation import gettext_lazy as _

class DroneTelemetry(models.Model):
    timestamp = models.IntegerField(primary_key=True, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    altitude = models.FloatField(null=False)
    vertical_speed = models.FloatField(null=False)
    speed = models.FloatField(null=False)
    heading = models.FloatField(null=False)
    battery_voltage = models.FloatField(null=False)

class DroneSingleton(models.Model):
    class ModeOptions(models.TextChoices):
        AUTO = "AUT", _("Auto")
        RTL = "RTL", _("Return to Land")
        MANUAL = "MAN", _("Manual")
        FAILSAFE = "FSF", _("Failsafe")

    mode = models.CharField(null=False, choices=ModeOptions, default=ModeOptions.AUTO)
    armed = models.CharField(default=False)

    # Singleton Stuff
    class Meta:
        abstract = True    

    def save(self, *args, **kwargs):
        self.pk = 1
        super(DroneSingleton, self).save(*args, **kwargs)   

    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    