from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import crud, serializers, models


class CreateElevatorSystemViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ElevatorViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorSerializer

    @action(methods=["get"], detail=True)
    def mark_maintenance(self, request, pk):
        elevator = crud.mark_maintainance(elevator_id=pk)
        serializer = serializers.ElevatorSerializer(elevator)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def get_elevator_direction(self, request, pk):
        elevator_direction = crud.get_elevator_direction_up_or_down(elevator_id=pk)
        return Response({"status": elevator_direction})

    @action(methods=["get"], detail=True)
    def get_next_destination_floor(self, request, pk):
        elevator_destination_floor = crud.get_destination_floor_for_elevator(
            elevator_id=pk
        )
        return Response({"Next Destination Floor": elevator_destination_floor})

    @action(methods=["patch"], detail=True)
    def elevator_door_status(self, request, pk=None, door=None):
        elevator = crud.update_elevator_door_status(elevator_id=pk, door=door)
        serializer = serializers.ElevatorSerializer(elevator)
        return Response(serializer.data)


class CreateElevatorRequestViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorRequestSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def move_elevator(self, request, *args, **kwargs):
        crud.move_elevator_by_one_floor()
        return Response({"status": "Elevator moved one floor successfully"})

    @action(methods=["get"], detail=True)
    def get_elevator_requests(self, request, pk=None, done=None):
        elevator_requests = crud.get_elevator_requests_for_elevator(
            elevator_id=pk, done=done
        )
        serializer = serializers.ElevatorRequestSerializer(elevator_requests, many=True)
        return Response(serializer.data)
