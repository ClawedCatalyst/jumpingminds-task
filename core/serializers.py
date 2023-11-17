from rest_framework import serializers

from . import crud, models


class ElevatorSystemSerializer(serializers.ModelSerializer):
    elevators = serializers.IntegerField()

    class Meta:
        model = models.ElevatorSystem
        fields = ["name", "no_of_floors", "elevators"]

    def create(self, data):
        no_of_elevators = data["elevators"]
        elevator_system = crud.create_elevator_system(
            name=data["name"], no_of_floors=data["no_of_floors"]
        )
        crud.create_n_elevators(
            no_of_elevators=no_of_elevators, elevator_system=elevator_system
        )
        return data


class ElevatorRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ElevatorRequest
        fields = ["elevator", "to_floor", "from_floor", "request_status"]
        extra_kwargs = {
            "elevator": {"read_only": True, "required": False},
        }

    def create(self, data):
        from_floor = data["from_floor"]
        to_floor = data["to_floor"]

        closest_elevator = crud.get_closest_available_elevator(from_floor=from_floor)

        create_elevator_request = crud.create_elevator_request(
            to_floor=to_floor, from_floor=from_floor, closest_elevator=closest_elevator
        )

        return create_elevator_request
