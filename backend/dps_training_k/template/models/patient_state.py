from django.db import models


class PatientState(models.Model):
    stateID = models.IntegerField(
        help_text="state number as it is used in original data set"
    )
    patientID = (
        models.IntegerField()
    )  # thinking about doing this with relations instead
    data = models.JSONField(help_text="data for patient in current phase")
    phase = models.IntegerField(help_text="current phase, e.g. 3")
    is_dead = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "stateID",
            "patientID",
        )
