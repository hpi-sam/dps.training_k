from django.db import models

from game.channel_notifications import PatientInstanceDispatcher
from helpers.actions_queueable import ActionsQueueable
from helpers.eventable import Eventable
from template.models.patient_state import PatientState
from .scheduled_event import ScheduledEvent


class PatientInstance(Eventable, ActionsQueueable, models.Model):
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
        null=True,  # for debugging purposes
        blank=True,  # for debugging purposes
    )
    patient_state = models.ForeignKey(
        PatientState,
        on_delete=models.SET_NULL,
        null=True,  # for debugging purposes
        default=None,  # for debugging purposes
    )
    patient_id = models.IntegerField(
        unique=True,
        help_text="patient_id used to log into patient - therefore part of authentication",
    )
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        PatientInstanceDispatcher.save_and_notify(self, changes, *args, **kwargs)

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with ID {self.patient_id}"

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

    def schedule_state_change(self):
        from game.models import ScheduledEvent

        if self.patient_state.is_dead:
            return False
        if self.patient_state.is_final():
            return False
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "execute_state_change",
            patient=self,
        )

    def execute_state_change(self):
        if self.patient_state.is_dead or self.patient_state.is_final():
            raise Exception(
                "Patient is dead or in final state, state change should have never been scheduled"
            )
        state_change_requirements = {"self.condition_checker.now()": ""}
        future_state = self.patient_state.transition.activate(state_change_requirements)
        if not future_state:
            return False
        self.patient_state = future_state
        self.save(update_fields=["patient_state"])
        self.schedule_state_change()
        return True

    def is_dead(self):
        if self.patient_state.is_dead:
            return True
        return False

    def serialize(self):
        return {
            "patientId": self.patient_id,
            "patientName": self.name,
            "patientCode": 3,  # ToDo: replace with actual patientCode
            "triage": self.triage,
        }
