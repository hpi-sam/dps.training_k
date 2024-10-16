from unittest.mock import patch

from django.test import TestCase

from .factories import (
    AreaFactory,
    LabFactory,
    PatientFactory,
    MaterialInstanceFactory,
    ActionInstanceFactory,
    PersonnelFactory,
)
from .mixin import TestUtilsMixin


class ResourceAssignmentTestCase(TestCase, TestUtilsMixin):
    def setUp(self):
        self.area = AreaFactory()
        self.lab = LabFactory()
        self.patient = PatientFactory()
        self.material_instance = MaterialInstanceFactory(area=self.area)
        self.personnel = PersonnelFactory(area=self.area)

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
        After a resource is assigned, a resource assignment event is sent to the consumer.
        """
        self.deactivate_live_updates()
        self.material_instance.try_moving_to(self.area)
        # as the resource is already assigned to the area, no notification should be sent
        self.assertEqual(_notify_exercise_update.call_count, 0)
        self.assertEqual(_notify_group.call_count, 0)

        self.material_instance.try_moving_to(self.lab)
        self.assertEqual(
            _notify_exercise_update.call_count, 1
        )  # lab should be outside of area -> exercise update
        self.assertEqual(_notify_group.call_count, 1)  # + assignment

        self.material_instance.try_moving_to(self.patient)
        self.assertEqual(
            _notify_exercise_update.call_count, 2
        )  # patient should be inside of area again -> exercise update
        self.assertEqual(
            _notify_group.call_count, 3
        )  # + assignment & + continuous_variable
        self.activate_live_updates()

    def test_resource_block_and_release(self):
        """
        Iff an action is running, the resources cannot be reassigned.
        """
        action_instance = ActionInstanceFactory(patient_instance=self.patient)
        self.material_instance.block(action_instance)
        self.assertFalse(self.material_instance.try_moving_to(self.area)[0])
        self.assertFalse(self.material_instance.try_moving_to(self.lab)[0])
        self.assertFalse(self.material_instance.try_moving_to(self.patient)[0])
        self.material_instance.release()
        # moving directly to the area won't work as it is already there
        self.assertTrue(self.material_instance.try_moving_to(self.lab)[0])
        self.assertTrue(self.material_instance.try_moving_to(self.area)[0])
        self.assertTrue(self.material_instance.try_moving_to(self.patient)[0])

    def test_resource_availability(self):
        """
        Resource holder can be checked for assigned and available resources.
        """

        # fails here
        self.assertEqual(
            self.patient.material_assigned(self.material_instance.template),
            [],
        )
        self.assertEqual(
            self.patient.material_available(self.material_instance.template),
            [],
        )
        self.assertEqual(self.patient.personnel_assigned(), [])
        self.assertEqual(self.patient.personnel_available(), [])
        self.assertEqual(
            self.area.material_assigned(self.material_instance.template),
            [self.material_instance],
        )
        self.assertEqual(
            self.area.material_available(self.material_instance.template),
            [self.material_instance],
        )
        self.assertEqual(self.area.personnel_assigned(), [self.personnel])
        self.assertEqual(self.area.personnel_available(), [self.personnel])

        self.material_instance.patient_instance = self.patient
        self.material_instance.area = None
        self.material_instance.save(update_fields=["patient_instance", "area"])

        self.personnel.area = None
        self.personnel.patient_instance = self.patient
        self.personnel.save(update_fields=["area", "patient_instance"])

        self.assertEqual(
            self.patient.material_assigned(self.material_instance.template),
            [self.material_instance],
        )
        self.assertEqual(
            self.patient.material_available(self.material_instance.template),
            [self.material_instance],
        )
        self.assertEqual(self.patient.personnel_assigned(), [self.personnel])
        self.assertEqual(self.patient.personnel_available(), [self.personnel])
        self.assertEqual(
            self.area.material_assigned(self.material_instance.template), []
        )
        self.assertEqual(
            self.area.material_available(self.material_instance.template), []
        )
        self.assertEqual(self.area.personnel_assigned(), [])
        self.assertEqual(self.area.personnel_available(), [])
