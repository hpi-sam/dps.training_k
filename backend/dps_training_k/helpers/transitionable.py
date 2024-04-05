# from game.models import ScheduledEvent moved down to avoid cicular imports


class Transitionable:
    """
    This mixin provides table-based state transition logic.
    """

    def schedule_state_transition(self):
        from game.models import ScheduledEvent

        if self.patient_state.is_dead:
            return False
        if self.patient_state.is_final():
            return False
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "execute_state_change",
            patient=self,
        )

    def execute_state_change(self):
        if self.patient_state.is_dead or self.patient_state.is_final():
            raise Exception(
                "Patient is dead or in final state, state change should have never been scheduled"
            )
        state_change_requirements = {"self.condition_checker.now()": ""}
        future_state = self.patient_state.transition.activate(
            state_change_requirements
        )  # Thoughts: This line is against law of demeter, the inderection is very long. how do we shorten this?
        # I want to keep the logic inside the state_transition, cause thsi is where it logically belongs.
        if not future_state:
            return False
        self.patient_state = future_state
        self.save()
        return True
