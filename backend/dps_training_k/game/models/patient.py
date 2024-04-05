from django.db import models
from django.conf import settings
from helpers.eventable import Eventable
from helpers.transitionable import Transitionable
from .scheduled_event import ScheduledEvent
from template.models.patient_state import PatientState


class Patient(Transitionable, Eventable, models.Model):
    class Triage(models.TextChoices):
        UNDEFINED = "-", "undefined"
        RED = "R", "red"
        YELLOW = "Y", "yellow"
        GREEN = "G", "green"
        Airway = "A", "airway"
        BREATHING = "B", "breathing"
        CIRCULATION = "C", "circulation"
        DISABILITY = "D", "disability"
        EXPOSURE = "E", "exposure"

    name = models.CharField(
        max_length=100, default="Max Mustermann"
    )  # technically patientData but kept here for simplicity for now
    # patientCode = models.ForeignKey()  # currently called "SensenID"
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    area = models.ForeignKey(
        "Area",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    patient_state = models.ForeignKey(
        PatientState,
        on_delete=models.SET_NULL,
        null=True,  # for debugging purposes
        default=None,  # for debugging purposes
    )
    patientId = models.IntegerField(
        help_text="patientId used to log into patient - therefore part of authentication"
    )
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with ID {self.patientId}"

    # ToDo: remove after actual method is implemented
    def schedule_temporary_event(self):
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "temporary_event_test",
            patient=self,
        )

    def temporary_event_test(self):
        print("temporary_event_test called")
        return True

    def is_dead(self):
        if self.patient_state.is_dead:
            return True
        return False
