from django.db import models
from .scheduled_event import ScheduledEvent

# from game.channel_notifications import AppliedActionDispatcher


class AppliedActionState(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    FINISHED = "FI", "finished"
    ACTIVE = "AC", "active"

    DECLINED = "DE", "declined"
    CANCELED = "CA", "canceled"


class AppliedActionTimestamp(models.Model):
    applied_action = models.OneToOneField(
        "AppliedAction",
        on_delete=models.CASCADE,
    )
    state_name = models.CharField(choices=AppliedActionState.choices, max_length=2)
    t_local_begin = models.IntegerField(
        blank=True,
        null=True,
    )
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )


class AppliedAction(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_type = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    state = models.CharField(
        choices=AppliedActionState.choices,
        default=AppliedActionState.PLANNED,
        max_length=2,
    )
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )

    @property
    def name(self):
        return self.action_template.name
    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        # AppliedActionDispatcher.save_and_notify(self, changes, *args, **kwargs)

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
            state=AppliedActionState.DECLINED,
            reason_of_declination=context,
        )

    def start_application(self):
        ScheduledEvent.create_event(
            self.patient.exercise,
            self.action_type.duration,  # ToDo: Replace with scalable local time system
            "application_finished",
            applied_action=self,
        )
        self.state = AppliedActionState.IN_PROGRESS
        self.save(update_fields=["state"])

    def application_finished(self):
        self.state = AppliedActionState.FINISHED
        self.save(update_fields=["state"])
