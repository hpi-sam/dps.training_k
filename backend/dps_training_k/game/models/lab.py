from django.db import models

from helpers.moveable_to import MoveableTo


class Lab(MoveableTo):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def can_receive_actions(self):
        return True

    @staticmethod
    def frontend_model_name():
        return "Labor"

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
