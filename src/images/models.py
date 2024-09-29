from django.db import models

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
        VISIBLE = 'visible', 'Visible'
        THERMAL = 'thermal', 'Thermal'
    
    image = models.ImageField(upload_to='files/', null=False)
    title = models.CharField(max_length=100)
    image_type = models.CharField(max_length=20, 
                                  choices=ImageType.choices, 
                                  default=ImageType.VISIBLE)
    taken_at = models.DateTimeField(null=False)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    altitude = models.FloatField(null=True)

    
    def __str__(self):
        return self.taken_at.strftime('%Y-%m-%d %H:%M:%S')

    