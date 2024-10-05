from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Image(models.Model):
    """Represents an image taken by the drone.

    Args:
        image (models.ImageField): The image file.
        title (models.CharField): The title of the image.
        image_type (models.CharField): The type of image.
        taken_at (models.DateTimeField): The time the image was received.
        longitude (models.FloatField): The longitude where the image was taken.
        latitude (models.FloatField): The latitude where the image was taken.
        altitude (models.FloatField): The altitude where the image was taken.
    """

    class ImageType(models.TextChoices):
        """Represents the type of image.

        Options:
            VISIBLE: A visible light image.
            THERMAL: A thermal (IR) image.
        """

        VISIBLE = "visible", "Visible"
        THERMAL = "thermal", "Thermal"

    image = models.ImageField(upload_to="files/", null=False)
    title = models.CharField(max_length=100)
    image_type = models.CharField(
        max_length=20, choices=ImageType.choices, default=ImageType.VISIBLE
    )
    taken_at = models.DateTimeField(null=False)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)

    def __str__(self):
        return self.taken_at.strftime("%Y-%m-%d %H:%M:%S")


class ObjectType(models.TextChoices):
    STANDARD = "standard", _("Standard")
    EMERGENT = "emergent", _("Emergent")


class Color(models.TextChoices):
    BLACK = "black", _("Black")
    RED = "red", _("Red")
    BLUE = "blue", _("Blue")
    GREEN = "green", _("Green")
    PURPLE = "purple", _("Purple")
    BROWN = "brown", _("Brown")
    ORANGE = "orange", _("Orange")


class Shape(models.TextChoices):
    CIRCLE = "circle", _("Circle")
    SEMI_CIRCLE = "semicircle", _("Semi-Circle")
    QUARTER_CIRCLE = "quartercircle", _("Quarter-Circle")
    TRIANGLE = "triangle", _("Triangle")
    RECTANGLE = "rectangle", _("Rectangle")
    PENTAGON = "pentagon", _("Pentagon")
    STAR = "star", _("Star")
    CROSS = "cross", _("Cross")


class GroundObject(models.Model):
    """Represents a ground object, either emergent or standard, detected by the system.

    Attributes:
        id (UUID): Primary key, unique identifier for each ground object
        object_type (ObjectType): Type of the ground object (standard or emergent)
        lat (float): Latitude of the ground object
        long (float): Longitude of the ground object
        shape (Shape): Shape of the ground object
        color (Color): Color of the ground object
        text (str): Text displayed on the ground object
        text_color (Color): Color of the text displayed on the ground object
    """

    id = models.UUIDField(primary_key=True, editable=False, unique=True)
    object_type = models.CharField(
        max_length=10, choices=ObjectType.choices, default=ObjectType.STANDARD
    )
    lat = models.FloatField(null=False)
    long = models.FloatField(null=False)
    shape = models.CharField(max_length=15, choices=Shape.choices, default=Shape.CIRCLE)
    color = models.CharField(max_length=10, choices=Color.choices, default=Color.BLACK)
    text = models.CharField(max_length=100, null=False, blank=True)
    text_color = models.CharField(
        max_length=10, choices=Color.choices, default=Color.BLACK
    )

    class Meta:
        verbose_name = _("Ground Object")
        verbose_name_plural = _("Ground Objects")
