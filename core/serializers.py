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
