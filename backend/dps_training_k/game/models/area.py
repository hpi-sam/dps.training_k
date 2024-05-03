from django.db import models

from helpers.actions_queueable import ActionsQueueable
from game.channel_notifications import AreaDispatcher


class Area(ActionsQueueable, models.Model):
    name = models.CharField(max_length=30)
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    inventory = models.OneToOneField(
        "Inventory", on_delete=models.CASCADE, null=True, blank=True
    )
    isPaused = models.BooleanField()

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
        AreaDispatcher.save_and_notify(self, update_fields, super(), *args, **kwargs)
