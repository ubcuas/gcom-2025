from django.db import models
from django.utils.translation import gettext_lazy as _


class DroneTelemetry(models.Model):
    """Represents the telemetry data of the drone at an instance in time.

    Attributes:
        timestamp (int): The UNIX timestamp of the telemetry data
        latitude (float): The latitude of the drone
        longitude (float): The longitude of the drone
        altitude (float): The altitude of the drone
        vertical_speed (float): The vertical speed of the drone
        speed (float): The speed of the drone
        heading (float): The heading of the drone
        battery_voltage (float): The battery voltage of the drone
    """

    timestamp = models.IntegerField(primary_key=True, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    altitude = models.FloatField(null=False)
    vertical_speed = models.FloatField(null=False)
    speed = models.FloatField(null=False)
    heading = models.FloatField(null=False)
    battery_voltage = models.FloatField(null=False)


class DroneSingleton(models.Model):
    """Represents the connected drone.

    There can only be one drone connected to the system at a time.

    Attributes:
        mode (ModeOptions): The mode the drone is in
        armed (bool): Whether the drone is armed
    """

    class ModeOptions(models.TextChoices):
        """Defines the modes the drone can be in

        Attributes:
            AUTO: The drone is in autonomous mode
            RTL: The drone is returning to land
            MANUAL: The drone is in manual mode
            FAILSAFE: The drone is in failsafe mode
        """

        AUTO = "AUT", _("Auto")
        RTL = "RTL", _("Return to Land")
        MANUAL = "MAN", _("Manual")
        FAILSAFE = "FSF", _("Failsafe")

    mode = models.CharField(
        max_length=3, choices=ModeOptions.choices, default=ModeOptions.AUTO
    )
    armed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Drone Singleton")
        verbose_name_plural = _("Drone Singleton")

    def save(self, *args, **kwargs):
        """Overrides the save method to ensure only one instance exists"""
        self.pk = 1
        super(DroneSingleton, self).save(*args, **kwargs)

    def delete(self):
        """Overrides the delete method to prevent deletion"""
        pass

    @classmethod
    def load(cls):
        """Loads the singleton instance from the database if present, otherwise creates it"""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    # Singleton instance holder
    _instance = None

    @classmethod
    def get_instance(cls):
        """Returns the singleton instance"""
        if cls._instance is None:
            cls._instance = cls.load()
        return cls._instance

    @classmethod
    def reset_instance(cls):
        """Resets the singleton instance"""
        cls._instance = None
