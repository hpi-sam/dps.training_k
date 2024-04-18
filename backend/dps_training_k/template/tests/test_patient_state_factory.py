from django.test import TestCase
from template.models import PatientState, StateTransition
from template.tests.factories import PatientStateFactory


class PatientStateFactoryTestCase(TestCase):

    def setUp(self):
        self.depth = 10
        self.transition_count = 2

    def test_not_overcreating_depth(self):
        """
        After the specified transitions (first parameter) happened, no further states might be reached
        """
        patient_state_count = PatientState.objects.count()
        patient_state = PatientStateFactory(self.depth, self.transition_count)
        self.assertEqual(
            patient_state_count + self.depth * self.transition_count + 1,
            PatientState.objects.count(),
        )

        local_patient_state = patient_state
        for i in range(self.depth):
            self.assertIsNotNone(local_patient_state.transition.resulting_state)
            local_patient_state = local_patient_state.transition.resulting_state
        self.assertIsNone(local_patient_state.transition.resulting_state)

    def test_not_overcreating_height(self):
        """
        After the specified conditions (second parameter) happened, no further conditions might be reached
        """
        patient_state_transition_count = StateTransition.objects.count()
        patient_state = PatientStateFactory(self.depth, self.transition_count)
        self.assertEqual(
            patient_state_transition_count + self.depth * self.transition_count + 1,
            StateTransition.objects.count(),
        )

        local_patient_state = PatientStateFactory(self.depth, self.transition_count)
        local_transition = local_patient_state.transition
        for i in range(self.transition_count - 1):
            self.assertIsNotNone(local_transition.next_state_transition)
            local_transition = local_transition.next_state_transition
        self.assertIsNone(local_transition.next_state_transition)
