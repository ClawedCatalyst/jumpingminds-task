from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers


class CreateElevatorSystemViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorSystemSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class CreateElevatorRequestViewSet(ModelViewSet):
    serializer_class = serializers.ElevatorRequestSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
