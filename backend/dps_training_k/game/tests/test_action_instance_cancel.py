import uuid
from unittest.mock import patch

from django.test import TestCase

from template.tests.factories import ActionFactory, MaterialFactory
from .factories import (
    ActionInstanceFactory,
    MaterialInstanceFactory,
    PatientFactory,
    PersonnelFactory,
)
from .mixin import TestUtilsMixin
from ..models import ActionInstanceStateNames


class CancelAction(TestUtilsMixin, TestCase):
    def setUp(self):
        self._start_application_patch = patch(
            "game.models.ActionInstance._start_application"
        )
        self._start_application_patch.start()
        self.material_1 = MaterialFactory(
            name="Material 1", reusable=True, uuid=str(uuid.uuid4())
        )
        self.material_2 = MaterialFactory(
            name="Material 2", reusable=False, uuid=str(uuid.uuid4())
        )
        self.patient = PatientFactory()
        self.personnel = PersonnelFactory(patient_instance=self.patient)
        self.action_instance = ActionInstanceFactory(
            template=ActionFactory(), patient_instance=self.patient
        )

    def tearDown(self):
        self._start_application_patch.stop()

    def test_action_state_cancelable(self):
        """
        An Action can only be canceled if its state is either running, planned or on_hold
        """

        self.assertTrue(self.action_instance.cancel()[0])
        self.assertEqual(
            self.action_instance.state_name, ActionInstanceStateNames.CANCELED
        )
        self.action_instance._update_state(ActionInstanceStateNames.IN_PROGRESS)
        self.assertTrue(self.action_instance.cancel()[0])
        self.action_instance._update_state(ActionInstanceStateNames.ON_HOLD)
        self.assertTrue(self.action_instance.cancel()[0])
        self.action_instance._update_state(ActionInstanceStateNames.IN_EFFECT)
        self.assertEqual(
            self.action_instance.cancel(),
            (
                False,
                f"Aktionen mit dem Status {ActionInstanceStateNames.IN_EFFECT.label} können nicht abgebrochen werden.",
            ),
        )
        self.assertEqual(
            self.action_instance.current_state.name, ActionInstanceStateNames.IN_EFFECT
        )
        self.action_instance._update_state(ActionInstanceStateNames.FINISHED)
        self.assertFalse(self.action_instance.cancel()[0])
        self.action_instance._update_state(ActionInstanceStateNames.CANCELED)
        self.assertFalse(self.action_instance.cancel()[0])
        self.action_instance._update_state(ActionInstanceStateNames.EXPIRED)
        self.assertFalse(self.action_instance.cancel()[0])

    def test_canceling_action(self):
        """
        If an action is canceled, the materials and personnel used for the action are freed and the consumable materials are deleted iff the action
        was already running.
        """
        material_instance_1 = MaterialInstanceFactory(
            template=self.material_1,
            patient_instance=self.action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            template=self.material_2,
            patient_instance=self.action_instance.patient_instance,
        )

        self.assertEqual(self.patient.personnel_available(), [self.personnel])

        self.personnel.block(action_instance=self.action_instance)
        material_instance_1.block(action_instance=self.action_instance)
        material_instance_2.block(action_instance=self.action_instance)
        self.action_instance._update_state(ActionInstanceStateNames.IN_PROGRESS)
        self.assertEqual(self.patient.personnel_available(), [])
        self.assertEqual(self.patient.material_available(self.material_1), [])
        self.assertEqual(self.patient.material_available(self.material_2), [])

        self.action_instance.cancel()

        self.assertEqual(self.patient.personnel_available(), [self.personnel])
        self.assertEqual(
            self.patient.material_available(self.material_1), [material_instance_1]
        )
        self.assertEqual(self.patient.material_available(self.material_2), [])
