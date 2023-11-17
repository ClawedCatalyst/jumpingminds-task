from . import models


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
