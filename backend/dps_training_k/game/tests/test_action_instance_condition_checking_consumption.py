import uuid
import copy
from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from template.tests.factories import MaterialFactory, ConditionFactory, ActionFactory
from .factories import (
    ActionInstanceFactory,
    MaterialInstanceFactory,
    PatientFactory,
    PersonnelFactory,
    AreaFactory,
    LabFactory,
)
from .mixin import TestUtilsMixin
from ..models import MaterialInstance
from template.models import Action


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
        self.assertEqual(action_template.material_needed(), [])
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        self.assertEqual(
            action_instance._verify_acquiring_resources(
                action_instance.attached_instance(), action_instance.attached_instance()
            ),
            ([], "", True),
        )

    def test_action_check(self):
        """
        Each group of the material condition is satisfied by at least one material. The personnel condition is satisfied.
        """
        action_template = ActionFactory(conditions=self.material_personnel_condition)
        self.assertIn(
            [self.material_1, self.material_2], action_template.material_needed()
        )
        self.assertIn([self.material_3], action_template.material_needed())
        self.assertEqual(action_template.personnel_count_needed(), 1)

        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        aquired_resources, message, conditions_satisfied = (
            action_instance._verify_acquiring_resources(
                action_instance.attached_instance(), action_instance.attached_instance()
            )
        )
        self.assertEqual(conditions_satisfied, False)
        self.assertNotEqual(message, "")

        personnel = PersonnelFactory(patient_instance=action_instance.patient_instance)
        material_instance_1 = MaterialInstanceFactory(
            template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        aquired_resources, message, conditions_satisfied = (
            action_instance._verify_acquiring_resources(
                action_instance.attached_instance(), action_instance.attached_instance()
            )
        )
        self.assertTrue(conditions_satisfied)

    def test_blocking(self):
        """
        After an action was applied successfully, the used resources are blocked
        """
        # This enforces ActionInstance.try_application to succeed, so that the blocking phase is guaranteed to be reached
        self.deactivate_moving()
        self.can_receive_actions_patch = patch(
            "game.models.PatientInstance.can_receive_actions"
        )
        self.can_receive_actions_patch.start().return_value = True
        self.is_absent_patch = patch("game.models.PatientInstance.is_absent")
        self.is_absent_patch.start().return_value = False
        self.deactivate_relocating()

        action_template = ActionFactory(conditions=self.material_personnel_condition)
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        personnel = PersonnelFactory(patient_instance=action_instance.patient_instance)
        material_instance_1 = MaterialInstanceFactory(
            template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        succeeded, message = action_instance.try_application()
        self.assertTrue(succeeded)
        material_instance_1.refresh_from_db()
        material_instance_2.refresh_from_db()
        material_instance_3.refresh_from_db()
        personnel.refresh_from_db()
        self.assertTrue(material_instance_1.is_blocked())
        self.assertTrue(material_instance_3.is_blocked())
        self.assertFalse(material_instance_2.is_blocked())
        self.assertTrue(personnel.is_blocked())

        self.activate_moving()
        self.can_receive_actions_patch.stop()
        self.is_absent_patch.stop()
        self.activate_relocating()

    def test_consuming_freeing_resources(self):
        """
        After an action is finished, the materials and personnel used for the action are freed. Consumable materials are deleted.
        """
        # This enforces ActionInstance.try_application to succeed, so that the blocking phase is guaranteed to be reached
        self.deactivate_moving()
        self.can_receive_actions_patch = patch(
            "game.models.PatientInstance.can_receive_actions"
        )
        self.can_receive_actions_patch.start().return_value = True
        self.is_absent_patch = patch("game.models.PatientInstance.is_absent")
        self.is_absent_patch.start().return_value = False
        self.deactivate_relocating()

        action_template = ActionFactory(conditions=self.material_personnel_condition)
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=PatientFactory()
        )
        personnel = PersonnelFactory(patient_instance=action_instance.patient_instance)
        self.material_1.is_reusable = False
        self.material_1.save(update_fields=["is_reusable"])

        material_instance_1 = MaterialInstanceFactory(
            template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        action_instance.try_application()
        action_instance._free_resources()
        action_instance._consume_resources()

        self.assertRaises(
            ObjectDoesNotExist, MaterialInstance.objects.get, pk=material_instance_1.id
        )
        material_instance_2.refresh_from_db()
        material_instance_3.refresh_from_db()
        personnel.refresh_from_db()
        self.assertFalse(material_instance_3.is_blocked())
        self.assertFalse(material_instance_2.is_blocked())
        self.assertFalse(personnel.is_blocked())

        self.activate_moving()
        self.can_receive_actions_patch.stop()
        self.is_absent_patch.stop()
        self.activate_relocating()

    @patch("game.models.MaterialInstance.can_move_to_type")
    def test_failed_check_is_transparent(self, can_move_to_type_material):
        """
        Integration Test: If the condition check fails, the action instance and all participating objects do not change.
        """
        can_move_to_type_material.return_value = True
        action_template = ActionFactory(
            conditions=self.material_personnel_condition,
            location=Action.Location.BEDSIDE,
        )
        patient_instance = PatientFactory()
        area = AreaFactory()
        action_instance = ActionInstanceFactory(
            template=action_template, patient_instance=patient_instance
        )
        personnel = PersonnelFactory(area=area)
        material_instance_1 = MaterialInstanceFactory(
            template=self.material_1,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_2 = MaterialInstanceFactory(
            template=self.material_2,
            patient_instance=action_instance.patient_instance,
        )
        material_instance_3 = MaterialInstanceFactory(
            template=self.material_3,
            patient_instance=action_instance.patient_instance,
        )
        old_state = copy.deepcopy(
            [
                patient_instance,
                area,
                personnel,
                material_instance_1,
                material_instance_2,
                material_instance_3,
            ]
        )
        self.assertFalse(
            action_instance.try_application()[0]
        )  # fail because of missing resource personnel
        new_state = [
            patient_instance,
            area,
            personnel,
            material_instance_1,
            material_instance_2,
            material_instance_3,
        ]
        self.assertEqual(old_state, new_state)

        self.assertTrue(personnel.try_moving_to(patient_instance)[0])
        action_template.category = Action.Category.EXAMINATION
        action_template.location = Action.Location.LAB
        action_template.relocates = True
        action_template.save(update_fields=["category", "location", "relocates"])
        action_instance = ActionInstanceFactory(
            template=action_template,
            patient_instance=patient_instance,
            lab=LabFactory(),
        )
        can_move_to_type_material.return_value = False
        old_state = copy.deepcopy(
            [
                patient_instance,
                area,
                personnel,
                material_instance_1,
                material_instance_2,
                material_instance_3,
            ]
        )
        self.assertFalse(
            action_instance.try_application()[0]
        )  # fail because of movement to lab is disallowed in mixin
        new_state = [
            patient_instance,
            area,
            personnel,
            material_instance_1,
            material_instance_2,
            material_instance_3,
        ]
        self.assertEqual(old_state, new_state)
