from django.db import models


class PatientState(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "state_id"], name="unique_code_stateid"
            )
        ]

    code = models.IntegerField(help_text="Sensen Code", default=0)
    state_id = models.IntegerField(
        help_text="For Debugging purposes! State number as it is used in original data set",
        default=0,
    )
    transition = models.ForeignKey(
        "StateTransition",
        on_delete=models.CASCADE,
    )
    vital_signs = models.JSONField(help_text="data for patient in current phase")
    examination_codes = models.JSONField(
        help_text="List of pairs of examination types and examination codes"
    )
    special_events = models.CharField(
        blank=True,
        null=True,
        help_text='Perceivable events of high priority, e.g. "Patient schreit vor Schmerzen"',
    )
    is_dead = models.BooleanField(default=False)

    def is_final(self):
        return self.transition.is_final()

    def __str__(self):
        return f"PatientState with code {self.code} and state id {self.state_id}"
