import sys

from django.db.models import F, Min, Func

from . import models


class ABS(Func):
    
    function = "ABS"

def create_elevator_system(name: str, no_of_floors: int) -> models.ElevatorSystem:
    elevator_system_obj = models.ElevatorSystem.objects.create(
        name=name, no_of_floors=no_of_floors
    )
    return elevator_system_obj


def create_n_elevators(
    no_of_elevators: int, elevator_system: models.ElevatorSystem
) -> str:
    elevator_obj = [
        models.Elevator(elevator_system=elevator_system) for i in range(no_of_elevators)
    ]
    models.Elevator.objects.bulk_create(elevator_obj)
    return "Done"


def get_closest_available_elevator(from_floor: int) -> models.Elevator:
    closest_available_elevator = (
        models.Elevator.objects.filter(current_status="available")
        .annotate(distance_to_requested=Min(ABS(F("current_floor") - from_floor)))
        .order_by("distance_to_requested")
        .first()
    )

    available_elevator_time = abs(closest_available_elevator.current_floor - from_floor)

    busy_elevators = models.Elevator.objects.filter(current_status="busy")
    busy_elevator_time = sys.maxsize
    
    if busy_elevators:
        closest_busy_elevator = busy_elevators[0]
        for elevator in busy_elevators:
            elevator_time_to_reach = 0
            elevator_requests = models.ElevatorRequest.objects.filter(
                elevator=elevator, request_status="in_process"
            ).order_by("-created_at")
            previous_floor = elevator.current_floor
            for elevator_request in elevator_requests:
                elevator_time_to_reach += abs(elevator_request.from_floor - previous_floor)
                elevator_time_to_reach += abs(
                    elevator_request.from_floor - elevator_request.to_floor
                )
                previous_floor = elevator_request.to_floor

            if elevator_time_to_reach < busy_elevator_time:
                closest_busy_elevator = elevator
                busy_elevators_time = elevator_time_to_reach

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
    return models.ElevatorRequest.objects.create(
        elevator=closest_elevator, to_floor=to_floor, from_floor=from_floor
    )
