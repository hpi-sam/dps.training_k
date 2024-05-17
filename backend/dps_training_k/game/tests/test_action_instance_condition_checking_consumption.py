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
from .mixin import TestUtilsMixin


class ActionCheckAndBlockingTestCase(TestUtilsMixin, TestCase):
    def setUp(self):
        self._start_application_patch = patch(
            "game.models.ActionInstance._start_application"
        )
        self._start_application_patch.start()
        self.material_1 = MaterialFactory(name="Material 1", uuid=str(uuid.uuid4()))
        self.material_2 = MaterialFactory(name="Material 2", uuid=str(uuid.uuid4()))
        self.material_3 = MaterialFactory(name="Material 3", uuid=str(uuid.uuid4()))
        self.material_personnel_condition = ConditionFactory(
            material=[
                [self.material_1.uuid, self.material_2.uuid],
                self.material_3.uuid,
            ],
            num_personnel=1,
        )
        self._empty_material_condition = ConditionFactory(material=[])
        self.deactivate_notifications()

    def tearDown(self):
        self._start_application_patch.stop()
        self.activate_notifications()

    def test_empty_condition(self):
        """
        ActionInstances with empty conditions may always be applied
        """
        action_template = ActionFactory(conditions=self._empty_material_condition)
        self.assertIsNone(action_template.material_needed())
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        self.assertEqual(
            action_instance.check_conditions_and_block_resources(
                action_instance.attached_instance(), action_instance.attached_instance()
            ),
            (True, None),
        )

    def test_action_check(self):
        """
        Each group of the material condition is satisfied by at least one material. The personnel condition is satisfied.
        """
        action_template = ActionFactory(conditions=self.material_personnel_condition)
        print(action_template.material_needed())
        self.assertIn(
            [self.material_1, self.material_2], action_template.material_needed()
        )
        self.assertIn([self.material_3], action_template.material_needed())
        self.assertEqual(action_template.personnel_count_needed(), 1)

        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        conditions_satisfied, _ = action_instance.check_conditions_and_block_resources(
            action_instance.attached_instance(), action_instance.attached_instance()
        )
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
        conditions_satisfied, _ = action_instance.check_conditions_and_block_resources(
            action_instance.attached_instance(), action_instance.attached_instance()
        )
        self.assertEqual((conditions_satisfied, _), (True, None))

    def test_blocking(self):
        """
        If a conditon is satisfied, the materials and the personnel used for satisfiction are blocked
        """
        action_template = ActionFactory(conditions=self.material_personnel_condition)
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
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
        conditions_satisfied, _ = action_instance.check_conditions_and_block_resources(
            action_instance.attached_instance(), action_instance.attached_instance()
        )
        material_instance_1.refresh_from_db()
        material_instance_2.refresh_from_db()
        material_instance_3.refresh_from_db()
        personnel.refresh_from_db()
        self.assertTrue(material_instance_1.is_blocked())
        self.assertTrue(material_instance_3.is_blocked())
        self.assertFalse(material_instance_2.is_blocked())
        self.assertTrue(personnel.is_blocked())
