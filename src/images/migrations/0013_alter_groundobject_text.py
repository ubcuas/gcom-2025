# Generated by Django 5.0.6 on 2024-10-11 23:18
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("images", "0012_alter_groundobject_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="groundobject",
            name="text",
            field=models.CharField(max_length=100),
        ),
    ]
