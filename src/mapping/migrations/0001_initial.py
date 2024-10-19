# Generated by Django 5.1.2 on 2024-10-19 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AreaOfInterest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("area_of_interest", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="MappingRoute",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("points_on_route", models.JSONField()),
                ("altitude", models.FloatField()),
            ],
        ),
    ]