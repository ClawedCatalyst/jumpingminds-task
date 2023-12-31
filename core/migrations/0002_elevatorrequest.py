# Generated by Django 4.2.7 on 2023-11-17 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ElevatorRequest",
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
                ("to_floor", models.PositiveIntegerField()),
                ("from_floor", models.PositiveIntegerField()),
                ("is_busy", models.BooleanField(default=False)),
                (
                    "elevator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="elevator_requests",
                        to="core.elevator",
                    ),
                ),
            ],
        ),
    ]
