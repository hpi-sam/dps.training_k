from django.test import TestCase
from template.tests.factories import PatientStateFactory


class PatientStateBuildingTestCase(TestCase):
    """A test for a testing thing(factory).
    I don't like this, but manually creating deeply nested objects seemed equally hard to read and
    equally error prone to me. If you disagree I would be happy to remove the PatientStateFactory.
    """

    def test_state_transition(self):
        patient_state = PatientStateFactory(2, 2)
        self.assertEqual(
            patient_state.transition.resulting_state.transition.resulting_state.transition.resulting_state,
            None,
        )
