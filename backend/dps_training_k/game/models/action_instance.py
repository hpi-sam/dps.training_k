from django.db import models
from game.models import ScheduledEvent


class ActionInstanceState(models.TextChoices):
    PLANNED = "PL", "planned"
    IN_PROGRESS = "IP", "in_progress"
    FINISHED = "FI", "finished"
    ACTIVE = "AC", "active"

    DECLINED = "DE", "declined"
    CANCELED = "CA", "canceled"


class ActionInstanceTimestamp(models.Model):
    applied_action = models.OneToOneField(
        "ActionInstance",
        on_delete=models.CASCADE,
    )
    state_name = models.CharField(choices=ActionInstanceState.choices, max_length=2)
    t_local_begin = models.IntegerField(
        blank=True,
        null=True,
    )
    t_local_end = models.IntegerField(
        blank=True,
        null=True,
    )


class ActionInstance(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_template = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    state = models.CharField(
        choices=ActionInstanceState.choices,
        default=ActionInstanceState.PLANNED,
        max_length=2,
    )
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )

    @property
    def name(self):
        return self.action_template.name

    @classmethod
    def try_application(cls, patient, action_template):
        is_applicable, context = action_template.application_status(
            patient, patient.area
        )
        if is_applicable:
            obj = cls.objects.create(patient=patient, action_template=action_template)
            obj.start_application()
            return obj
        return cls.objects.create(
            patient=patient,
            action_template=action_template,
            state=ActionInstanceState.DECLINED,
            reason_of_declination=context,
        )

    def start_application(self):
        ScheduledEvent.create_event(
            self.patient.exercise,
            self.action_template.duration,  # ToDo: Replace with scalable local time system
            "application_finished",
            applied_action=self,
        )
        self.state = ActionInstanceState.IN_PROGRESS
        self.save(update_fields=["state"])

    def application_finished(self):
        self.state = ActionInstanceState.FINISHED
        self.save(update_fields=["state"])
