from django.db import models
from helpers.eventable import Eventable
from .exercise import Exercise


class Patient(Eventable, models.Model):
    name = models.CharField(
        max_length=100, default="Max Mustermann"
    )  # technically patientData but kept here for simplicity for now
    # patientID = models.ForeignKey()  # currently called "SensenID"
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    # stateID = models.ForeignKey()
    # measureID = models.ManyToManyField()
    patientCode = models.IntegerField(
        help_text="patientCode used to log into patient - therefore part of authentication"
    )

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with code {self.patientCode}"
