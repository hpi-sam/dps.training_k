from django.db import models

from game.channel_notifications import PatientInstanceDispatcher
from helpers.actions_queueable import ActionsQueueable
from helpers.eventable import Eventable
from helpers.triage import Triage
from template.tests.factories import PatientStateFactory
from .scheduled_event import ScheduledEvent


class PatientInstance(Eventable, ActionsQueueable, models.Model):
    area = models.ForeignKey(
        "Area",
        on_delete=models.CASCADE,
    )
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Max Mustermann")
    patient_frontend_id = models.IntegerField(
        unique=True,
        help_text="patient_frontend_id used to log into patient - therefore part of authentication",
    )
    patient_state = models.ForeignKey(
        "template.PatientState",
        on_delete=models.SET_NULL,
        null=True,  # for debugging purposes
        default=None,  # for debugging purposes
    )
    static_information = models.ForeignKey(
        "template.PatientInformation",
        on_delete=models.CASCADE,
        null=True,  # for migration purposes
    )  # via Sensen ID
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )
    user = models.OneToOneField(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        from . import User

        if not self.pk:
            self.user, _ = User.objects.get_or_create(
                username=self.patient_frontend_id, user_type=User.UserType.PATIENT
            )
            self.user.set_password(
                self.exercise.exercise_frontend_id
            )  # Properly hash the password
            self.user.save()

            self.patient_state = PatientStateFactory(
                10, 2
            )  # temporary state for testing - should later take static_information into account

        changes = kwargs.get("update_fields", None)
        PatientInstanceDispatcher.save_and_notify(
            self, changes, super(), *args, **kwargs
        )

    def delete(self, using=None, keep_parents=False):
        self.user.delete()
        PatientInstanceDispatcher.delete_and_notify(self)

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

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with frontend ID {self.patient_frontend_id}"
