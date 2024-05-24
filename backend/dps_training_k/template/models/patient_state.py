from django.db import models


class PatientState(models.Model):
    stateID = models.IntegerField(
        help_text="For Debugging purposes! State number as it is used in original data set",
        default=0,
    )
    transition = models.ForeignKey("StateTransition", on_delete=models.CASCADE)
    vital_signs = models.JSONField(help_text="data for patient in current phase")
    examination_codes = models.JSONField(
        help_text="List of pairs of examination types and examination codes"
    )
    special_events = models.CharField(
        blank=True,
        null=True,
        help_text='Perceivable events of high priority, e.g. "Patient schreit vor Schmerzen"',
    )
    state_depth = models.IntegerField()
    is_dead = models.BooleanField(default=False)

    def is_final(self):
        return self.transition.is_final()
