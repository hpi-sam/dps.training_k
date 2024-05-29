from django.db import models
from typing import List


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

    def activate(self, conditions: List):
        if self.resulting_state is None:
            return None
        if not self.is_valid(conditions):
            return self.next_state_transition.activate(conditions)
        return self.resulting_state

    def is_valid(self, conditions: List):
        return self.get_root_logic_node().evaluate_tree(conditions)

    def is_final(self):
        return self.resulting_state is None
    
    def get_root_logic_node(self):
        for node in self.logic_nodes.all():
            if node.parent is None:
                return node
        raise Exception("No root node was found!")