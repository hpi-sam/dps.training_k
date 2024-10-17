from django.db import models

from helpers.models import UUIDable


class ContinuousVariable(UUIDable, models.Model):
    class Variable(models.TextChoices):
        SPO2 = "SpO2"
        HEART_RATE = "BPM"

    class Function(models.TextChoices):
        LINEAR = "linear"
        SIGMOID = ("sigmoid",)
        SIGMOID_DELAYED = ("delayed sigmoid",)
        INCREMENT = "increment"
        DECREMENT = "decrement"

    name = models.CharField(choices=Variable.choices, unique=True)
    function = models.CharField(choices=Function.choices)
    exceptions = models.JSONField()

    def __str__(self):
        return f"Continuous variable called {self.name}"
