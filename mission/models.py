import uuid
from django.db import models

# Create your models here.
class Mission(models.Model):
    id = models.UUIDField(primary_key=True, null=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)