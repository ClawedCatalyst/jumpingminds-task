from django.contrib import admin

from . import models

# Register your models here.

admin.site.register(models.Elevator)
admin.site.register(models.ElevatorSystem)
admin.site.register(models.ElevatorRequest)
