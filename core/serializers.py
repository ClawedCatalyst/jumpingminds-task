from rest_framework import serializers

from . import crud, models


class ElevatorSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ElevatorSystem
        fields = ["id", "name", "no_of_floors"]

    def create(self, data):
        no_of_elevators = data.get("elevators", 0)
        elevator_system = crud.create_elevator_system(
            name=data["name"], no_of_floors=data["no_of_floors"]
        )
        crud.create_n_elevators(
            no_of_elevators=no_of_elevators, elevator_system=elevator_system
        )
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        responseData = {"success": True}
        data["elevators-count"] = crud.get_elevators_count_from_elevator_system(
            elevator_system_id=data["id"]
        )
        responseData["data"] = data
        return data


class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Elevator
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        elevator_system = models.ElevatorSystem.objects.filter(
            id=data["elevator_system"]
        ).first()
        responseData = {"success": True}
        data["elevator_system"] = ElevatorSystemSerializer(elevator_system).data
        responseData["data"] = data
        return responseData


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        responseData = {"success": True}
        responseData["data"] = data
        return responseData
