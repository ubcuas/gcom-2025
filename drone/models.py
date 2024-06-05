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

    mode = models.CharField(max_length=3, choices=ModeOptions.choices, default=ModeOptions.AUTO)
    armed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Drone Singleton")
        verbose_name_plural = _("Drone Singleton")

    def save(self, *args, **kwargs):
        self.pk = 1
        super(DroneSingleton, self).save(*args, **kwargs)   

    def delete(self, *args, **kwargs):
        pass
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    # Singleton instance holder
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.load()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        cls._instance = None
