from django.db import models

from game.channel_notifications import AreaDispatcher
from helpers.actions_queueable import ActionsQueueable


class Area(ActionsQueueable, models.Model):
    name = models.CharField(unique=True, max_length=30)
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    isPaused = models.BooleanField()
    # labID = models.ForeignKey("Lab")

    @classmethod
    def create_area(cls, name, exercise, isPaused=False):
        unique_name = name
        number = 1

        # Loop until a unique name is found
        while cls.objects.filter(name=unique_name).exists():
            unique_name = f"{name}{number}"
            number += 1

        return cls.objects.create(
            name=unique_name, exercise=exercise, isPaused=isPaused
        )

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        AreaDispatcher.save_and_notify(self, update_fields, *args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        AreaDispatcher.delete_and_notify(self)

    def serialize(self):
        from game.models import Personnel
        from game.models import PatientInstance

        return {
            "areaName": self.name,
            "patients": [
                patient.serialize()
                for patient in PatientInstance.objects.filter(area=self)
            ],
            "personnel": [
                personnel.serialize()
                for personnel in Personnel.objects.filter(area=self)
            ],
            "material": [],  # TODO: implement material
        }
