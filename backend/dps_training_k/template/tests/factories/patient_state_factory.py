import factory
from template.models import PatientState
from .state_transition_factory import StateTransitionFactory
from .state_data_factory import StateDataFactory
from template.models import StateTransition


class EmptyPatientStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientState
        django_get_or_create = ("transition", "data", "state_depth", "is_dead")

    transition = factory.SubFactory(StateTransitionFactory)
    data = factory.LazyFunction(lambda: StateDataFactory())
    state_depth = 1
    is_dead = False


class PatientStateFactory:
    """
    Generates complex of states and transitions to be used by a patient.
    The complex uses the same list of transitions for states of the same depth
    :param depth: The number of states after the initial state
    :param transition_count: The number of follow up states per state
    """

    def __new__(cls, depth=1, transition_count=1):
        """Needed to copy interface of factory_boy factories"""
        instance = super().__new__(cls)
        instance.__init__(depth, transition_count)
        return instance.generate()

    def __init__(self, depth, transition_count):
        if depth < 0:
            raise ValueError("Depth must be greater than or equal to 0")
        if transition_count < 0:
            raise ValueError("Transitions must be greater than or equal to 0")
        self.depth = depth
        self.transition_count = transition_count

    def generate(self):
        self.initial_state = EmptyPatientStateFactory(transition=None)
        self._generate(self.depth, self.transition_count, self.initial_state)
        return self.initial_state

    def _generate(self, depth, transition_count, initial_state):
        previous_states = [initial_state]
        for i in range(depth):
            current_state_transitions = self._generate_chained_transitions(
                transition_count
            )
            current_states = self._generate_Patient_States(transition_count)
            for i in range(transition_count):
                current_state_transitions[i].resulting_state = current_states[i]
                current_state_transitions[i].save()

            for state in previous_states:
                state.transition = current_state_transitions[0]
                state.save()

            previous_states = current_states
        for state in previous_states:
            state.transition = StateTransitionFactory()
            state.save()

    def _generate_chained_transitions(self, transition_count):
        current_state_transitions = [StateTransitionFactory()]
        current_transition_count = 1

        while current_transition_count < transition_count:
            current_state_transitions.insert(
                0,
                StateTransitionFactory(
                    next_state_transition=current_state_transitions[0]
                ),
            )
            current_transition_count += 1

        return current_state_transitions

    def _generate_Patient_States(self, transition_count):
        return [
            EmptyPatientStateFactory(transition=None, state_depth=i)
            for i in range(transition_count)
        ]  # vielleicht immer das selbe
