from django.db import models


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
