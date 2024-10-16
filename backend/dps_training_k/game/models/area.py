from django.db import models

from game.channel_notifications import AreaDispatcher
from helpers.moveable_to import MoveableTo


class Area(MoveableTo, models.Model):

    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    isPaused = models.BooleanField(default=False)
    name = models.CharField(max_length=30)

    @classmethod
    def create_area(cls, name, exercise, isPaused=False):
        unique_name = name
        number = 1

        # Loop until a unique name is found
        while cls.objects.filter(name=unique_name, exercise=exercise).exists():
            unique_name = f"{name} {number}"
            number += 1

        return cls.objects.create(
            name=unique_name, exercise=exercise, isPaused=isPaused
        )

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields", None)
        AreaDispatcher.save_and_notify(self, update_fields, super(), *args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        AreaDispatcher.delete_and_notify(self)

    @staticmethod
    def frontend_model_name():
        return "Bereich"

    def __str__(self):
        return f"{self.name} of exercise {self.exercise.frontend_id}"
