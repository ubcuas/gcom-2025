# Generated by Django 5.0.6 on 2024-10-11 05:30
import uuid

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0008_alter_groundobject_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groundobject",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("4049f277-ee38-45ff-90e8-10f5a2c01563"),
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
