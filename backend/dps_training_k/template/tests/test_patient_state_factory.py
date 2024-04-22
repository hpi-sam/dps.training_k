from django.test import TestCase
from template.models import PatientState, StateTransition
from template.tests.factories import PatientStateFactory


class PatientStateFactoryTestCase(TestCase):

    def setUp(self):
        self.depth = 10
        self.transition_count = 2
        self.patient_state = PatientStateFactory(self.depth, self.transition_count)

    def test_patient_state_transitions_amount(self):
        """
        The amount of states equals depth * transition_count + 1 (initial state)
        The amount of transitions equals depth * transition_count + 2 (final states)
        """
        self.assertEqual(
            self.depth * self.transition_count + 1,
            PatientState.objects.count(),
        )
        self.assertEqual(
            self.depth * self.transition_count + 2,
            StateTransition.objects.count(),
        )

    def test_iterating_states(self):
        """
        After the specified transitions (first parameter) happened, no further states might be reached
        """
        local_patient_state = self.patient_state
        for i in range(self.depth):
            self.assertIsNotNone(local_patient_state.transition.resulting_state)
            local_patient_state = local_patient_state.transition.resulting_state
        self.assertIsNone(local_patient_state.transition.resulting_state)

    def test_iterating_transitions(self):
        """
        After the specified conditions (second parameter) happened, no further conditions might be reached
        """
        local_transition = self.patient_state.transition
        for i in range(self.transition_count - 1):
            self.assertIsNotNone(local_transition.next_state_transition)
            local_transition = local_transition.next_state_transition
        self.assertIsNone(local_transition.next_state_transition)
