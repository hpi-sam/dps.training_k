from django.db import models
from typing import Dict


class StateTransition(models.Model):
    resulting_state = models.ForeignKey(
        "PatientState",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    next_state_transition = models.ForeignKey(
        "StateTransition", on_delete=models.CASCADE, null=True, blank=True
    )

    def activate(self, conditions: Dict):
        if self.resulting_state is None:
            return None
        if not self.is_valid(conditions):
            return self.next_state_transition.activate(conditions)
        return self.resulting_state

    def is_valid(self, conditions: Dict):
        # ToDo: This is a stub, should be replaced by old backend logic, specifically condition.is_fulfilled(self, subconditions_dict)
        return True

    def is_final(self):
        return self.resulting_state is None
