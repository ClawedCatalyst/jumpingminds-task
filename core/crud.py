import sys

from django.db.models import F, Func, Min
from rest_framework.exceptions import ValidationError

from . import models


class ABS(Func):
    # Custom function for absolute value
    function = "ABS"


def create_elevator_system(name: str, no_of_floors: int) -> models.ElevatorSystem:
    # Create an elevator system instance
    elevator_system_obj = models.ElevatorSystem.objects.create(
        name=name, no_of_floors=no_of_floors
    )
    return elevator_system_obj


def create_n_elevators(
    no_of_elevators: int, elevator_system: models.ElevatorSystem
) -> str:
    # Create multiple elevator instances and associate them with the elevator system
    elevator_obj = [
        models.Elevator(elevator_system=elevator_system) for i in range(no_of_elevators)
    ]
    models.Elevator.objects.bulk_create(elevator_obj)
    return "Done"


def get_closest_available_elevator(from_floor: int) -> models.Elevator:
    # Find the closest available elevator based on the requested floor
    closest_available_elevator = (
        models.Elevator.objects.filter(current_status="available")
        .annotate(distance_to_requested=Min(ABS(F("current_floor") - from_floor)))
        .order_by("distance_to_requested")
        .first()
    )
    # Calculate time to reach the available elevator
    available_elevator_time = abs(closest_available_elevator.current_floor - from_floor)

    # Find the closest busy elevator
    busy_elevators = models.Elevator.objects.filter(current_status="busy")
    busy_elevator_time = sys.maxsize

    if busy_elevators:
        closest_busy_elevator = busy_elevators[0]
        for elevator in busy_elevators:
            elevator_time_to_reach = 0
            elevator_requests = models.ElevatorRequest.objects.filter(
                elevator=elevator, request_status="in_process"
            ).order_by("-created")
            previous_floor = elevator.current_floor
            for elevator_request in elevator_requests:
                elevator_time_to_reach += abs(
                    elevator_request.from_floor - previous_floor
                )
                elevator_time_to_reach += abs(
                    elevator_request.from_floor - elevator_request.to_floor
                )
                previous_floor = elevator_request.to_floor

            # Update the closest busy elevator if it reaches faster
            if elevator_time_to_reach < busy_elevator_time:
                closest_busy_elevator = elevator
                busy_elevators_time = elevator_time_to_reach

    # Choose the closest elevator (available or busy) based on time
    if available_elevator_time < busy_elevator_time:
        closest_available_elevator.next_floor = from_floor
        closest_available_elevator.current_status = "busy"
        closest_available_elevator.door_status = "close"
        closest_available_elevator.save()
        return closest_available_elevator
    else:
        return closest_busy_elevator


def create_elevator_request(
    to_floor: int, from_floor: int, closest_elevator: models.Elevator
) -> models.ElevatorRequest:
    # Create an elevator request for the chosen elevator
    return models.ElevatorRequest.objects.create(
        elevator=closest_elevator, to_floor=to_floor, from_floor=from_floor
    )


def move_elevator_by_one_floor():
    # Move busy elevators by one floor based on their current requests
    elevators = models.Elevator.objects.filter(current_status="busy")
    for elevator in elevators:
        elevator_request = (
            models.ElevatorRequest.objects.filter(
                elevator=elevator, request_status__in=["in_process", "in_service"]
            )
            .order_by("created")
            .first()
        )

        if elevator_request:
            if (
                elevator_request.request_status == "in_process"
                and elevator.current_floor < elevator_request.to_floor
            ):
                # Move elevator up one floor
                elevator.current_floor += 1
                if elevator.current_floor == elevator_request.to_floor:
                    elevator_request.request_status = "in_service"
                elevator_request.save()
                elevator.save()
            elif (
                elevator_request.request_status == "in_process"
                and elevator.current_floor > elevator_request.to_floor
            ):
                # Move elevator down one floor
                elevator.current_floor -= 1
                if elevator.current_floor == elevator_request.to_floor:
                    elevator_request.request_status = "in_service"
                elevator_request.save()
                elevator.save()
            elif (
                elevator_request.request_status == "in_process"
                and elevator.current_floor == elevator_request.to_floor
            ):
                # Mark the request as in service if the elevator has reached the target floor
                elevator_request.request_status = "in_service"
                elevator_request.save()
            elif (
                elevator_request.request_status == "in_service"
                and elevator.current_floor < elevator_request.from_floor
            ):
                # Move elevator up one floor for returning to the original floor
                elevator.current_floor += 1
                if elevator.current_floor == elevator_request.from_floor:
                    elevator_request.request_status = "done"
                    elevator.current_status = "available"
                elevator_request.save()
                elevator.save()
            elif (
                elevator_request.request_status == "in_service"
                and elevator.current_floor > elevator_request.from_floor
            ):
                # Move elevator down one floor for returning to the original floor
                elevator.current_floor -= 1
                if elevator.current_floor == elevator_request.from_floor:
                    elevator_request.request_status = "done"
                    elevator.current_status = "available"
                elevator_request.save()
                elevator.save()


def mark_maintainance(elevator_id: int) -> models.Elevator:
    elevator = models.Elevator.objects.filter(id=elevator_id).first()
    if not elevator:
        pass
        # TODO validation when elevator does not exits with given elevator id

    if elevator.current_status != "maintenance":
        elevator.current_status = "maintenance"
        elevator.door_status = "closed"
    else:
        elevator.current_status = "available"
    elevator.save()
    return elevator


def get_elevators_count_from_elevator_system(elevator_system_id: int) -> int:
    return models.Elevator.objects.filter(elevator_system=elevator_system_id).count()


def get_elevator_direction_up_or_down(elevator_id: int) -> str:
    elevator = models.Elevator.objects.filter(id=elevator_id).first()
    if elevator is None:
        raise ValidationError(
            f"Elevator with the given id: {elevator_id} does not exist"
        )
    if elevator.current_status == "available":
        return f"Elevator with id: {elevator_id} is available, not moving"

    if elevator.current_status == "maintenance":
        return f"Elevator with id: {elevator_id} is under maintenance"

    if elevator.current_floor < elevator.next_floor:
        return f"Elevator with {elevator_id} is moving up"
    else:
        return f"Elevator with id: {elevator_id} is moving down"


def get_elevator_requests_for_elevator(elevator_id: int, done: bool or None):
    if done:
        return models.ElevatorRequest.objects.filter(
            elevator=elevator_id, request_status="done"
        )
    else:
        return models.ElevatorRequest.objects.filter(elevator=elevator_id)


def get_destination_floor_for_elevator(elevator_id: int):
    elevator = models.Elevator.objects.filter(id=elevator_id).first()
    return elevator.next_floor


def update_elevator_door_status(
    elevator_id: int or None, door: int or None
) -> models.Elevator:
    elevator = models.Elevator.objects.filter(elevator=elevator_id).first()
    if elevator.current_status == "maintenance":
        raise ValidationError(
            {"error": f"Elevator with id: {elevator_id} is currently under maintenance"}
        )

    if door and elevator.current_status == "busy":
        raise ValidationError(
            {
                "error": f"Elevator with id: {elevator_id} is currently busy, door cannot be open"
            }
        )
    if door:
        elevator.door_status = "open"
        elevator.save()
    else:
        elevator.door_status = "close"
        elevator.save()

    return elevator
