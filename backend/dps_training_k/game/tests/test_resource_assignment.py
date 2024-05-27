from django.test import TestCase
from unittest.mock import patch
from .mixin import TestUtilsMixin
from .factories import (
    AreaFactory,
    LabFactory,
    PatientFactory,
    MaterialInstanceFactory,
    ActionInstanceFactory,
)


class ResourceAssignmentTestCase(TestCase, TestUtilsMixin):
    def setUp(self):
        self.area = AreaFactory()
        self.lab = LabFactory()
        self.patient = PatientFactory()
        self.material_instance = MaterialInstanceFactory(area=self.area)

    def test_assigning_resources(self):
        """
        Resources(Material, Personnel) can be assigned to a patient, area or lab.
        """

        self.material_instance.try_moving_to(self.area)
        self.assertEqual(self.material_instance.attached_instance(), self.area)
        self.material_instance.try_moving_to(self.lab)
        self.assertEqual(self.material_instance.attached_instance(), self.lab)
        self.material_instance.try_moving_to(self.patient)
        self.assertEqual(self.material_instance.attached_instance(), self.patient)

    @patch(
        "game.channel_notifications.MaterialInstanceDispatcher._notify_exercise_update"
    )
    @patch("game.channel_notifications.MaterialInstanceDispatcher._notify_group")
    def test_channel_notifications_being_send(
        self, _notify_group, _notify_exercise_update
    ):
        """
        After a resource is assigned, a resource assignment event is send to the consumer.
        """
        self.deactivate_live_updates()
        self.material_instance.try_moving_to(self.area)
        self.assertEqual(_notify_exercise_update.call_count, 0)
        self.assertEqual(_notify_group.call_count, 1)

        self.material_instance.try_moving_to(self.lab)
        self.assertEqual(_notify_exercise_update.call_count, 0)
        self.assertEqual(_notify_group.call_count, 2)

        self.material_instance.try_moving_to(self.patient)
        self.assertEqual(_notify_exercise_update.call_count, 0)
        self.assertEqual(_notify_group.call_count, 3)
        self.activate_live_updates()

    def test_resource_assignment_during_running_action(self):
        """
        Iff an action is running, the resources cannot be reassigned.
        """
        action_instance = ActionInstanceFactory(patient_instance=self.patient)
        self.material_instance.block(action_instance)
        self.assertFalse(self.material_instance.try_moving_to(self.area))
        self.assertFalse(self.material_instance.try_moving_to(self.lab))
        self.assertFalse(self.material_instance.try_moving_to(self.patient))
        self.material_instance.release()
        self.assertTrue(self.material_instance.try_moving_to(self.area))
        self.assertTrue(self.material_instance.try_moving_to(self.lab))
        self.assertTrue(self.material_instance.try_moving_to(self.patient))
