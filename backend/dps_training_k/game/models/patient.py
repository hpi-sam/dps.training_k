from django.db import models
from django.conf import settings
from helpers.eventable import Eventable
from helpers.transitionable import Transitionable
from .scheduled_event import ScheduledEvent
from template.models.patient_state import PatientState


class Patient(Eventable, models.Model):
    name = models.CharField(
        max_length=100, default="Max Mustermann"
    )  # technically patientData but kept here for simplicity for now
    # patientID = models.ForeignKey()  # currently called "SensenID"
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    stateID = models.OneToOneField(
        "template.PatientState",
        on_delete=models.SET_NULL,
        null=True,
        default=settings.DEFAULT_STATE_ID,
    )
    # measureID = models.ManyToManyField()
    patientCode = models.IntegerField(
        help_text="patientCode used to log into patient - therefore part of authentication"
    )

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with code {self.patientCode}"

    # ToDo remove when actual method is implemented
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

    def schedule_state_transition(self):
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "transition_state",
            patient=self,
        )

    def transition_state(self):
        next_state = self.determine_next_state()
        self.state = next_state
        return True
