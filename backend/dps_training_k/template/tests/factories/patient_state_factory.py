import factory

from template.models import PatientState
from .state_data_factories import VitalSignsData, ExaminationCodesData
from .state_transition_factory import StateTransitionFactory


class EmptyPatientStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientState
        django_get_or_create = (
            "code",
            "state_id",
            "transition",
            "vital_signs",
            "examination_codes",
            "special_events",
            "is_dead",
        )
    
    code = factory.Sequence(lambda n: n + 1000)
    state_id = factory.Sequence(lambda n: n + 100)
    transition = factory.SubFactory(StateTransitionFactory)
    vital_signs = factory.LazyFunction(VitalSignsData)
    examination_codes = factory.LazyFunction(ExaminationCodesData)
    special_events = None
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
        initial_state = EmptyPatientStateFactory.build(transition=None)
        states = [initial_state]
        old_transitions = self._generate_chained_transitions()
        states[0].transition = old_transitions[0]
        states[0].save()
        for i in range(2, self.depth + 2):
            states = self._generate_Patient_States()
            new_transitions = self._generate_chained_transitions()
            for j in range(self.transition_count):
                states[j].transition = new_transitions[j]
                states[j].save()
            for j in range(self.transition_count):
                old_transitions[j].resulting_state = states[j]
                old_transitions[j].save()
            old_transitions = new_transitions
        return initial_state

    def _generate_chained_transitions(self):
        current_state_transitions = [StateTransitionFactory()]
        for _ in range(self.transition_count - 1):
            current_state_transitions.insert(
                0,
                StateTransitionFactory(
                    next_state_transition=current_state_transitions[0]
                ),
            )

        return current_state_transitions

    def _generate_Patient_States(self):
        return [
            EmptyPatientStateFactory.build(transition=None)
            for i in range(self.transition_count)
        ]
