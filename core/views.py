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
        elevator = crud.get_elevator_direction_up_or_down(elevator_id=pk)
        return Response({"status": elevator})


class CreateElevatorRequestViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorRequestSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def move_elevator(self, request, *args, **kwargs):
        crud.move_elevator_by_one_floor()
        return Response({"status": "Elevator moved one floor successfully"})
