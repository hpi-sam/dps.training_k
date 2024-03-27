class Transitionable:
    """
    This mixin provides table-based state transition logic.
    This class assumes that we are using the PatientState directly and not an InstanceClass
    """

    def execute_state_change(self):
        if self.is_dead():
            return False
        # ToDo: Add actual logic, remove stub
        next_state_id = self.determine_next_state(self.state.id)
        if not next_state_id:
            return False
        self.state = self.states.get(pk=next_state_id)
        return True

    def stub_determine_next_state(self, current_state):
        while not self.states.get(pk=current_state + 1):
            if current_state % 10:
                return None
            current_state += 1
        return current_state + 1


# ToDo: Implement Stub for now
# ToDo: Imoprt old componenent from old dps
# ToDo: Update to amount based logic
