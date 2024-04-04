class Transitionable:
    """
    This mixin provides table-based state transition logic.
    This class assumes that we are using the PatientState directly and not an InstanceClass
    """

    def execute_state_change(self):
        if self.is_dead():
            return False
        # ToDo: Add actual logic, remove stub
        future_state = self.stub_determine_next_state(self.state.id)
        if not future_state:
            return False
        self.state = future_state
        return True

    def stub_determine_next_state(self, current_state):
        while not self.state.is_dead and self.state.is_final():

# ToDo: Implement Stub for now
# ToDo: Imoprt old componenent from old dps
# ToDo: Update to amount based logic
