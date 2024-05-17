import uuid
from unittest.mock import patch
from django.test import TestCase
from template.tests.factories import MaterialFactory, ConditionFactory, ActionFactory
from .factories import (
    ActionInstanceFactory,
    MaterialInstanceFactory,
    PatientFactory,
    PersonnelFactory,
)


class ActionCheckAndBlockingTestCase(TestCase):
    def setUp(self):
        self._start_application_patch = patch("game.models.action.start_application")
        self._start_application_patch.start()
        self.material_1 = MaterialFactory(name="Material 1", uuid=uuid.uuid4())
        self.material_2 = MaterialFactory(name="Material 2", uuid=uuid.uuid4())
        self.material_3 = MaterialFactory(name="Material 3", uuid=uuid.uuid4())
        self.material_personnel_condition = ConditionFactory(
            material=[
                [self.material_1.uuid, self.material_2.uuid],
                self.material_3.uuid,
            ],
            num_personnel=1,
        )
        self._empty_material_condition = ConditionFactory(material=None)

    def tearDown(self):
        self._start_application_patch.stop()

    def test_empty_condition(self):
        """
        ActionInstances with empty conditions may always be applied
        """
        action_template = ActionFactory(conditions=self._empty_material_condition)
        self.assertIsNone(action_template.material_needed())
        action_instance = ActionInstanceFactory(
            action=action_template, patient_instance=PatientFactory()
        )
        self.assertEqual(action_instance.try_application(), (True, None))

    def test_action_check(self):
        """
        Each group of the material condition is satisfied by at least one material. The personnel condition is satisfied.
        """
        action_template = ActionFactory(conditions=self.material_condition)
        self.assertEqual(
            action_template.material_needed(),
            [
                [
                    self.material_1,
                    self.material_2,
                ],
                [self.material_3],
            ],
        )
        self.assertEqual(action_template.personnel_count_needed(), 1)

        action_instance = ActionInstanceFactory(
            action=action_template, patient_instance=PatientFactory()
        )
        conditions_satisfied, _ = action_instance.try_application()
        self.assertEqual(conditions_satisfied, False)
        personnel = PersonnelFactory(assigned_patient=action_instance.patient_instance)
        material_instance_1 = MaterialInstanceFactory(
            material_template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            material_template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            material_template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        conditions_satisfied, _ = action_instance.try_application()
        self.assertEqual((conditions_satisfied, _), (True, None))

    def test_blocking(self):
        """
        If a conditon is satisfied, the materials used for satisfiction and the personnel are blocked
        """
        action_template = ActionFactory(conditions=self.material_condition)
        action_instance = ActionInstanceFactory(
            action=action_template, patient_instance=PatientFactory()
        )
        personnel = PersonnelFactory(assigned_patient=action_instance.patient_instance)
        material_instance_1 = MaterialInstanceFactory(
            material_template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            material_template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            material_template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        conditions_satisfied, _ = action_instance.try_application()
        self.assertTrue(personnel.is_blocked())
        self.assertTrue(material_instance_1.is_blocked())
        self.assertTrue(material_instance_3.is_blocked())
        self.assertFalse(material_instance_2.is_blocked())
