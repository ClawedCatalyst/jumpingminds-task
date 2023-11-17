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
        "move-elevators",
        views.CreateElevatorRequestViewSet.as_view({"get": "move_elevator"}),
    ),
]
