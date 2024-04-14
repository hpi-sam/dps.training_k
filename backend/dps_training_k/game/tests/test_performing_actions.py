from django.test import TestCase
from game.models import ScheduledEvent, ActionInstance, ActionInstanceStateNames
from .factories.action_instance_factory import (
    PatientFactory,
)
from template.tests.factories import ActionFactory
from unittest.mock import patch


class ActionInstanceTestCase(TestCase):
    def setUp(self):
        self.application_status_patch = patch(
            "template.models.Action.application_status"
        )
        self.get_local_time_patch = patch("game.models.ActionInstance.get_local_time")
        self.application_status = self.application_status_patch.start()
        self.get_local_time = self.get_local_time_patch.start()
        self.get_local_time.return_value = 10
        self.application_status.return_value = True, None

    def tearDown(self):
        self.application_status_patch.stop()
        self.get_local_time_patch.stop()

    def test_action_creation(self):
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.PLANNED)

        self.application_status.return_value = False, "Not applicable"
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.DECLINED)

    def test_action_starting(self):
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.try_application()
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        self.application_status.return_value = False, "Not applicable"
        with self.assertRaises(ValueError):
            action_instance.try_application()

    @patch("game.channel_notifications.ActionInstanceDispatcher._notify_action_event")
    def test_channel_notifications_being_send(self, _notify_action_event):
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.try_application()
        self.assertEqual(_notify_action_event.call_count, 1)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        self.application_status.return_value = False, "Not applicable"
        action_instance.try_application()
        self.assertEqual(_notify_action_event.call_count, 2)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)
