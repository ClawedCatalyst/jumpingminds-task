from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from . import serializers
from . import crud


class CreateElevatorSystemViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CreateElevatorRequestViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorRequestSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def move_elevator(self, request, *args, **kwargs):
        crud.move_elevator_by_one_floor()
        return Response({"Elevator moved one floor successfully"})
