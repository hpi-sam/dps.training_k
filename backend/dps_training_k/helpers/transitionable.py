class Transitionable:
    """
    This mixin provides table-based state transition logic.
    """

    def execute_state_change(self):
        if self.is_dead():
            return False
        # ToDo: Add actual logic, remove stub
        state_change_requirements = {"self.condition_checker.now()": ""}
        future_state = self.state.transition.activate(state_change_requirements)
        if not future_state:
            return False
        self.state = future_state
        self.save()
        return True
