# Generated by Django 5.0.6 on 2024-09-21 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="DroneSingleton",
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
                (
                    "mode",
                    models.CharField(
                        choices=[
                            ("AUT", "Auto"),
                            ("RTL", "Return to Land"),
                            ("MAN", "Manual"),
                            ("FSF", "Failsafe"),
                        ],
                        default="AUT",
                        max_length=3,
                    ),
                ),
                ("armed", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Drone Singleton",
                "verbose_name_plural": "Drone Singleton",
            },
        ),
        migrations.CreateModel(
            name="DroneTelemetry",
            fields=[
                ("timestamp", models.IntegerField(primary_key=True, serialize=False)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("altitude", models.FloatField()),
                ("vertical_speed", models.FloatField()),
                ("speed", models.FloatField()),
                ("heading", models.FloatField()),
                ("battery_voltage", models.FloatField()),
            ],
        ),
    ]
