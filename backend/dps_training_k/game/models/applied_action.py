from typing import Iterable
from django.db import models
from .scheduled_event import ScheduledEvent
from game import channel_notifications


class AppliedAction(models.Model):
    """This is a dirty version for Testing, clean up later on"""

    class State(models.TextChoices):
        PLANNED = "PL", "planned"
        IN_PROGRESS = "IP", "in_progress"
        FINISHED = "FI", "finished"
        ACTIVE = "AC", "active"

        DECLINED = "DE", "declined"
        CANCELED = "CA", "canceled"

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_type = models.ForeignKey("template.ActionType", on_delete=models.CASCADE)
    state = models.CharField(choices=State.choices, default=State.PLANNED, max_length=2)
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )
    result = models.JSONField(null=True, blank=True, default=None)

    @property
    def name(self):
        return self.action_type.name

    @property
    def area(self):
        return self.patient.area

    @property
    def exercise(self):
        return self.patient.exercise

    @classmethod
    def try_application(cls, patient, action_type):
        is_applicable, context = action_type.application_status(patient, patient.area)
        if is_applicable:
            obj = cls.objects.create(patient=patient, action_type=action_type)
            obj.start_application()
            return obj
        return cls.objects.create(
            patient=patient,
            action_type=action_type,
            state=cls.State.DECLINED,
            reason_of_declination=context,
        )

    def start_application(self):
        ScheduledEvent.create_event(
            self.exercise,
            self.action_type.duration,  # ToDo: Replace with scalable local time system
            "application_finished",
            action=self,
        )
        self.state = AppliedAction.State.IN_PROGRESS
        self.save()

    def application_finished(self):
        self.state = AppliedAction.State.FINISHED
        self.result = self.action_type.result(self.patient)
        self.save()

    def save(self):
        super().save()
        channel_notifications.chose_applied_action_notification_method(self)
