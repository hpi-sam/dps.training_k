from django.test import TestCase
from template.tests.factories import PatientStateFactory


class PatientStateBuildingTestCase(TestCase):

    def test_not_overcreating_depth(self):
        """
        After the specified transitions (first parameter) happened, no further states might be reached
        """
        patient_state = PatientStateFactory(2, 2)
        self.assertIsNone(
            patient_state.transition.resulting_state.transition.resulting_state.transition.resulting_state
        )

    def test_not_overcreating_height(self):
        """
        After the specified conditions (second parameter) happened, no further conditions might be reached
        """
        patient_state = PatientStateFactory(2, 2)
        self.assertIsNone(
            patient_state.transition.next_state_transition.next_state_transition
        )
