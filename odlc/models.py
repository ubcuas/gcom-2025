import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class CameraImage(models.Model):
    timestamp = models.IntegerField(primary_key=True,null=False)
    image = models.FileField(null=False)

class GroundObject(models.Model):
    class GroundObjectType(models.TextChoices):
        STANDARD = 'S', "standard"
        EMERGENT = 'E', "emergent"
    
    class Color(models.TextChoices):
        BLACK = 'BLK', 'black'
        RED = 'RED', 'red'
        BLUE = 'BLU', 'blue'
        GREEN = 'GRE', 'green'
        PURPLE = 'PUR', 'purple'
        BROWN = 'BWN', 'brown'
        ORANGE = 'ORG', 'orange'

    class Shape(models.TextChoices):
        CIRCLE = 'CIR', 'circle'
        SEMI_CIRCLE = 'SCR', 'semi_circle'
        QUARTER_CIRCLE = 'QCR', 'quarter_circle'
        TRIANGLE = 'TRI', 'triangle'
        RECTANGLE = 'RCT', 'rectangle'
        PENTAGON = 'PNT', 'pentagon'
        STAR = 'STR', 'star'
        CROSS = 'CRS', 'cross'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    type = models.CharField(max_length=1, choices=GroundObjectType, default='E')
    shape = models.CharField(max_length=3, choices=Shape, blank=True)
    color = models.CharField(max_length=3, choices=Color, blank=True)
    text = models.CharField(max_length=16, blank=True)
    text_color = models.CharField(max_length=3, choices=Color, blank=True)
    

    

    
