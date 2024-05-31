from unittest.mock import patch
from django.core.management import call_command


from django.test import TestCase
from .mixin import TestUtilsMixin
from .factories import PatientFactory, LabFactory
from template.models import Action
from game.models import ActionInstance


class RelocationTestCase(TestUtilsMixin, TestCase):
    def setUp(self):
        self.deactivate_moving()
        call_command("minimal_actions")
        self._deactivate_moving.return_value = (True, "")
        self.patient_instance = PatientFactory()
        self.lab = LabFactory(exercise=self.patient_instance.exercise)
        self.action_template = Action.objects.get(name="Trauma CT")
        self.action_instance = ActionInstance.create(
            self.action_template,
            patient_instance=self.patient_instance,
            lab=self.patient_instance.exercise.lab,
        )

    def tearDown(self):
        self.activate_moving()

    def test_moving_to_lab(self):
        """
        If the action is a relocating action _try_relocating moves patient_instance, remembering it's original area,
        """
        original_area = self.patient_instance.area
        is_applicable, context = self.action_instance._try_relocating()
        self.assertTrue(is_applicable)
        self.assertEqual(self.action_instance.destination_area, original_area)

    def test_moving_to_lab_relocating_action(self):
        """
        If the action isn't a relocating action _try_relocating doesn't move the patient_instance, returning (True, "")
        """
        self.action_template.relocates = False
        self.action_template.save(update_fields=["relocates"])
        self.action_instance = ActionInstance.create(
            self.action_template,
            patient_instance=self.patient_instance,
            lab=self.patient_instance.exercise.lab,
        )
        self.assertIsNone(self.action_instance.destination_area)
        is_applicable, context = self.action_instance._try_relocating()
        self.assertTrue(is_applicable)
        self.assertIsNone(self.action_instance.destination_area)

    def test_moving_to_lab_with_active_relocating_action(self):
        """
        Iff there is already an active relocating action for the patient_instance, the _try_relocating just returns a (False, some_string) tuple
        """
        is_applicable, context = self.action_instance._try_relocating()
        non_relocating_template = Action.objects.exclude(relocates=True).first()
        non_image_action_instance = ActionInstance.create(
            non_relocating_template,
            patient_instance=self.patient_instance,
            lab=self.patient_instance.exercise.lab,
        )
        is_applicable, context = non_image_action_instance.try_application()
        self.assertFalse(is_applicable)
        self.assertIsNotNone(context)
