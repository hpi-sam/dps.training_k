import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from game.models import (
    ScheduledEvent,
    ActionInstance,
    ActionInstanceStateNames,
    ActionInstanceState,
)
from game.tasks import check_for_updates
from template.tests.factories import ActionFactory
from .factories import PatientFactory, ActionInstanceFactory
from .mixin import TestUtilsMixin


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
        """
        ActionInstance initial state are influenced by the application status of the action template.
        """
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.PLANNED)

    def test_action_starting(self):
        """
        An action instance that was planned in the beginning enters on-hold state when the application cannot be started at the moment.
        """
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.assertTrue(action_instance.try_application())
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        self.application_status.return_value = False, "Not applicable"
        self.assertFalse(action_instance.try_application())
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)

    @patch("game.channel_notifications.ActionInstanceDispatcher._notify_action_event")
    def test_channel_notifications_being_send(self, _notify_action_event):
        """
        Once an action instance is started, the dispatcher detects it and detects the actual state.
        """
        self.application_status.return_value = True, None
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.try_application()
        # send action-list twice, send confirmation event once = 3
        self.assertEqual(_notify_action_event.call_count, 3)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.application_status.return_value = False, "Not applicable"
        action_instance.try_application()
        # send action-list 4 times, send confirmation event twice = 6
        self.assertEqual(_notify_action_event.call_count, 6)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)


class ActionInstanceScheduledTestCase(TestUtilsMixin, TestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.action_instance = ActionInstanceFactory(patient_instance=PatientFactory())
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)
        self.deactivate_notifications()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()

    def test_action_is_scheduled(self):
        """
        Once an action instance is started, it changes its state to finished after the scheduled time.
        """
        self.action_instance._start_application()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(10)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 0)
        self.action_instance.refresh_from_db()  # Necessary because the check_for_updates changes happen out of scope,
        # thus self.action_instance isn't refreshed automatically
        self.assertIn(
            self.action_instance.current_state.name,
            ActionInstanceState.success_states(),
        )
