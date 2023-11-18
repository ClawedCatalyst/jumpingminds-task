from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import crud, serializers, models


class CreateElevatorSystemViewSet(ModelViewSet):
    """
    ViewSet for creating Elevator Systems.
    """

    serializer_class = serializers.ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ElevatorViewSet(ModelViewSet):
    """
    ViewSet for Elevators with additional actions.
    """

    serializer_class = serializers.ElevatorSerializer

    @action(methods=["get"], detail=True)
    def mark_maintenance(self, request, pk):
        """
        Mark an elevator for maintenance.

        Args:
            request: The HTTP request.
            pk: The primary key of the elevator.

        Returns:
            Response: Serialized data of the updated elevator.
        """
        elevator = crud.mark_maintenance(elevator_id=pk)
        serializer = serializers.ElevatorSerializer(elevator)
        return Response(serializer.data)

    @action(methods=["get"], detail=True)
    def get_elevator_direction(self, request, pk):
        """
        Get the direction of an elevator.

        Args:
            request: The HTTP request.
            pk: The primary key of the elevator.

        Returns:
            Response: JSON response with the elevator direction.
        """
        elevator_direction = crud.get_elevator_direction_up_or_down(elevator_id=pk)
        response = {"success": True, "data": {"status": elevator_direction}}
        return Response(response, status=200)

    @action(methods=["get"], detail=True)
    def get_next_destination_floor(self, request, pk):
        """
        Get the next destination floor of an elevator.

        Args:
            request: The HTTP request.
            pk: The primary key of the elevator.

        Returns:
            Response: JSON response with the next destination floor.
        """
        elevator_destination_floor = crud.get_destination_floor_for_elevator(
            elevator_id=pk
        )
        response = {
            "success": True,
            "data": {"Next Destination Floor": elevator_destination_floor},
        }

        return Response(response, status=200)

    @action(methods=["patch"], detail=True)
    def elevator_door_status(self, request, pk=None, door=None):
        """
        Update the door status of an elevator.

        Args:
            request: The HTTP request.
            pk: The primary key of the elevator.
            door: The door status.

        Returns:
            Response: Serialized data of the updated elevator.
        """
        elevator = crud.update_elevator_door_status(elevator_id=pk, door=door)
        serializer = serializers.ElevatorSerializer(elevator)
        return Response(serializer.data)


class CreateElevatorRequestViewSet(ModelViewSet):
    """
    ViewSet for creating Elevator Requests with additional actions.
    """

    serializer_class = serializers.ElevatorRequestSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def move_elevator(self, request, *args, **kwargs):
        """
        Move elevators by one floor.

        Args:
            request: The HTTP request.
            args: Additional arguments.
            kwargs: Additional keyword arguments.

        Returns:
            Response: JSON response indicating the status of the operation.
        """
        crud.move_elevator_by_one_floor()
        response = {
            "success": True,
            "data": {"status": "Elevator moved one floor successfully"},
        }
        return Response(response, status=200)

    @action(methods=["get"], detail=True)
    def get_elevator_requests(self, request, pk=None, done=None):
        """
        Get elevator requests.

        Args:
            request: The HTTP request.
            pk: The primary key of the elevator.
            done: Filter requests based on whether they are done or not.

        Returns:
            Response: Serialized data of elevator requests.
        """
        elevator_requests = crud.get_elevator_requests_for_elevator(
            elevator_id=pk, done=done
        )
        serializer = serializers.ElevatorRequestSerializer(elevator_requests, many=True)
        return Response(serializer.data)
