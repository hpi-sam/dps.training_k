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
        If the action is an imaging action _try_imaging_setup moves patient_instance, remembering it's original area,
        """
        original_area = self.patient_instance.area
        is_applicable, context = self.action_instance._try_imaging_setup()
        self.assertTrue(is_applicable)
        self.assertEqual(self.action_instance.destination_area, original_area)

    def test_moving_to_lab_non_imaging_action(self):
        """
        If the action isn't an imaging action _try_imaging_setup doesn't move the patient_instance, returning (True, "")
        """
        self.assertIsNone(self.action_instance.destination_area)
        self.action_template.category = Action.Category.OTHER
        self.action_template.save(update_fields=["category"])
        is_applicable, context = self.action_instance._try_imaging_setup()
        self.assertTrue(is_applicable)
        self.assertIsNone(self.action_instance.destination_area)

    def test_moving_to_lab_with_active_imiging_action(self):
        """
        Iff there is already an active imaging action for the patient_instance, the _try_imaging_setup just returns a (False, some_string) tuple
        """
        imaging_instance_1 = ActionInstance.create(
            self.action_template,
            patient_instance=self.patient_instance,
            lab=self.patient_instance.exercise.lab,
        )
        is_applicable, context = imaging_instance_1._try_imaging_setup()
        imaging_instance_2 = ActionInstance.create(
            self.action_template,
            patient_instance=self.patient_instance,
            lab=self.patient_instance.exercise.lab,
        )
        is_applicable, context = imaging_instance_2._try_imaging_setup()
        self.assertFalse(is_applicable)
        self.assertIsNone(imaging_instance_2.destination_area)
