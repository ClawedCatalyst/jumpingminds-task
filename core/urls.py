from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"elevators", views.CreateElevatorSystemViewSet, basename="elevators")
router.register(
    r"elevator-request", views.CreateElevatorRequestViewSet, basename="elevator-request"
)
urlpatterns = [
    path("", include(router.urls)),
    path(
        "move-elevators/",
        views.CreateElevatorRequestViewSet.as_view({"get": "move_elevator"}),
    ),
    path(
        "mark-maintainance/<int:pk>/",
        views.ElevatorViewSet.as_view({"get": "mark_maintenance"}),
    ),
    path(
        "get-direction/<int:pk>/",
        views.ElevatorViewSet.as_view({"get": "get_elevator_direction"}),
    ),
    path(
        "get-elevator-requests/<int:pk>/<int:done>/",
        views.CreateElevatorRequestViewSet.as_view({"get": "get_elevator_requests"}),
    ),
    path(
        "get-next-destination-floor/<int:pk>/",
        views.ElevatorViewSet.as_view({"get": "get_next_destination_floor"}),
    ),
    path(
        "door-status/<int:pk>/<int:door>/",
        views.ElevatorViewSet.as_view({"patch": "elevator_door_status"}),
    ),
]
