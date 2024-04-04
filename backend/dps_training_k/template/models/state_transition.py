from django.db import models


class StateTransition(models.Model):
    resulting_state = models.ForeignKey(
        "PatientState", on_delete=models.CASCADE, null=True, blank=True
    )
    next_state_transition = models.ForeignKey(
        "StateTransition", on_delete=models.CASCADE, null=True, blank=True
    )
