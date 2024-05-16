from django.db import models


class Lab(models.Model):
    exercise = models.OneToOneField(
        "Exercise",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Lab: {self.exercise.frontend_id}"
