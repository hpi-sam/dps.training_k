from django.db import models


class PatientState(models.Model):
    stateID = models.IntegerField(
        help_text="For Debugging purposes! State number as it is used in original data set",
        default=0,
    )
    transition = models.ForeignKey(
        "StateTransition", on_delete=models.CASCADE, null=True, blank=True
    )
    data = models.JSONField(help_text="data for patient in current phase")
    state_depth = models.IntegerField()
    is_dead = models.BooleanField(default=False)

    def is_final(self):
        return self.transition.is_final()
