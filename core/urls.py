from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"elevators", views.CreateElevatorSystemViewSet, basename="elevators")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "elevators/move-elevators/",
        views.CreateElevatorRequestViewSet.as_view({"get": "move_elevator"}),
    ),
    path(
        "elevators/mark-maintainance/<int:pk>/",
        views.ElevatorViewSet.as_view({"get": "mark_maintenance"}),
    ),
]
