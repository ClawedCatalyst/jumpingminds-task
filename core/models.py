from django.db import models


class ElevatorSystem(models.Model):
    name = models.CharField(max_length=255)
    no_of_floors = models.PositiveIntegerField()


class Elevator(models.Model):
    ELEVATOR_STATUS_CHOICES = [
        ("available", "Available"),
        ("busy", "Busy"),
        ("maintenance", "Maintenance"),
    ]

    ELEVATOR_DOOR_CHOICES = [
        ("open", "Open"),
        ("close", "Close"),
    ]

    elevator_system = models.ForeignKey(
        ElevatorSystem, related_name="elevator_system", on_delete=models.CASCADE
    )
    current_status = models.CharField(
        max_length=20, choices=ELEVATOR_STATUS_CHOICES, default="available"
    )
    door_status = models.CharField(
        max_length=10, choices=ELEVATOR_DOOR_CHOICES, default="open"
    )
    current_floor = models.PositiveIntegerField(default=1)
    next_floor = models.PositiveIntegerField(default=1)
    previous_floor = models.PositiveIntegerField(default=1)


class ElevatorRequest(models.Model):
    elevator = models.ForeignKey(
        Elevator, related_name="elevator_requests", on_delete=models.CASCADE
    )
    to_floor = models.PositiveIntegerField()
    from_floor = models.PositiveIntegerField()
    is_busy = models.BooleanField(default=False)
