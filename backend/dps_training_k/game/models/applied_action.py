from django.db import models
from .scheduled_event import ScheduledEvent
class AppliedAction(models.Model):

    class State(models.TextChoices):
        PLANNED = "PL", "planned"
        IN_PROGRESS = "IP", "in_progress"
        FINISHED = "FI", "finished"
        ACTIVE = "AC", "active"

        DECLINED = "DE", "declined"
        CANCELED = "CA", "canceled"

    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    action_type = models.ForeignKey("template.Action", on_delete=models.CASCADE)
    state = models.CharField(choices=State.choices, default=State.PLANNED, max_length=2)
    reason_of_declination = models.CharField(
        max_length=100, null=True, blank=True, default=None
    )
