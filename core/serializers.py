from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import crud, models


class ElevatorSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the ElevatorSystem model.
    """

    class Meta:
        model = models.ElevatorSystem
        fields = ["id", "name", "no_of_floors"]

    def validate(self, data):
        """
        Validate the no_of_floors field to ensure it is an integer.

        Args:
            data (dict): The input data.

        Raises:
            ValidationError: If no_of_floors is not an integer.

        Returns:
            dict: The validated data.
        """
        no_of_floors = data["no_of_floors"]
        if not isinstance(no_of_floors, int):
            raise ValidationError(
                {"success": False, "data": {"error": "no_of_floors must be an integer"}}
            )

        return super().validate(data)

    def create(self, data):
        """
        Create an ElevatorSystem instance and associated elevators.

        Args:
            data (dict): The input data.

        Returns:
            dict: The input data.
        """
        data["elevators"] = self.initial_data["elevators"]
        elevator_system = crud.create_elevator_system(
            name=data["name"], no_of_floors=data["no_of_floors"]
        )
        crud.create_n_elevators(
            no_of_elevators=data["elevators"], elevator_system=elevator_system
        )
        return elevator_system

    def to_representation(self, instance):
        """
        Transform the representation of an ElevatorSystem instance.

        Args:
            instance: The ElevatorSystem instance.

        Returns:
            dict: The transformed representation.
        """
        data = super().to_representation(instance)
        responseData = {"success": True}
        try:
            data["elevators-count"] = self.initial_data["elevators"]
        except:
            data["elevators-count"] = crud.get_elevators_count_from_elevator_system(
                elevator_system_id=data["id"]
            )
        responseData["data"] = data
        return data


class ElevatorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Elevator model.
    """

    class Meta:
        model = models.Elevator
        fields = "__all__"

    def to_representation(self, instance):
        """
        Transform the representation of an Elevator instance.

        Args:
            instance: The Elevator instance.

        Returns:
            dict: The transformed representation.
        """
        data = super().to_representation(instance)
        elevator_system = models.ElevatorSystem.objects.filter(
            id=data["elevator_system"]
        ).first()
        responseData = {"success": True}
        data["elevator_system"] = ElevatorSystemSerializer(elevator_system).data
        responseData["data"] = data
        return responseData


class ElevatorRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for the ElevatorRequest model.
    """

    class Meta:
        model = models.ElevatorRequest
        fields = ["elevator", "to_floor", "from_floor", "request_status"]
        extra_kwargs = {
            "elevator": {"read_only": True, "required": False},
        }

    def validate(self, data):
        """
        Validate the from_floor and to_floor fields.

        Args:
            data (dict): The input data.

        Raises:
            ValidationError: If from_floor is equal to to_floor.

        Returns:
            dict: The validated data.
        """
        if data["from_floor"] == data["to_floor"]:
            raise ValidationError(
                {"success": False, "data": {"error": "You are at the same floor"}}
            )
        return super().validate(data)

    def create(self, data):
        """
        Create an ElevatorRequest instance and find the closest available elevator.

        Args:
            data (dict): The input data.

        Returns:
            models.ElevatorRequest: The created ElevatorRequest instance.
        """
        from_floor = data["from_floor"]
        to_floor = data["to_floor"]

        closest_elevator = crud.get_closest_available_elevator(from_floor=from_floor)

        create_elevator_request = crud.create_elevator_request(
            to_floor=to_floor, from_floor=from_floor, closest_elevator=closest_elevator
        )

        return create_elevator_request

    def to_representation(self, instance):
        """
        Transform the representation of an ElevatorRequest instance.

        Args:
            instance: The ElevatorRequest instance.

        Returns:
            dict: The transformed representation.
        """
        data = super().to_representation(instance)
        responseData = {"success": True}
        responseData["data"] = data
        return responseData
