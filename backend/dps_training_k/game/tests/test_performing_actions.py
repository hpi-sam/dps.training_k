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
        self.check_conditions_and_block_resources_patch = patch(
            "game.models.ActionInstance.check_conditions_and_block_resources"
        )
        self.get_local_time_patch = patch("game.models.ActionInstance.get_local_time")
        self.check_conditions_and_block_resources = (
            self.check_conditions_and_block_resources_patch.start()
        )
        self.get_local_time = self.get_local_time_patch.start()
        self.get_local_time.return_value = 10
        self.check_conditions_and_block_resources.return_value = True, None

    def tearDown(self):
        self.check_conditions_and_block_resources_patch.stop()
        self.get_local_time_patch.stop()

    def test_action_creation(self):
        """
        ActionInstance initial state are influenced by the application status of the action template.
        """
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.PLANNED)

    @patch("game.models.PatientInstance.can_receive_actions")
    def test_action_starting(self, can_receive_actions):
        """
        An action instance that was planned in the beginning enters on-hold state when the application cannot be started at the moment.
        """
        can_receive_actions.return_value = True
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        succeeded, message = action_instance.try_application()
        self.assertTrue(succeeded)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        self.check_conditions_and_block_resources.return_value = False, "Not applicable"
        condition_succeeded, _ = action_instance.try_application()
        self.assertFalse(condition_succeeded)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)

    @patch("game.models.PatientInstance.can_receive_actions")
    @patch("game.channel_notifications.ActionInstanceDispatcher._notify_action_event")
    def test_channel_notifications_being_send(
        self, _notify_action_event, can_receive_actions
    ):
        """
        Once an action instance is started, the dispatcher detects it and detects the actual state.
        """
        can_receive_actions.return_value = True
        self.check_conditions_and_block_resources.return_value = True, None
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.try_application()
        # send action-list twice, send confirmation event once = 3
        self.assertEqual(_notify_action_event.call_count, 3)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.check_conditions_and_block_resources.return_value = False, "Not applicable"
        action_instance.try_application()
        # send action-list 4 times, send confirmation event twice = 6
        self.assertEqual(_notify_action_event.call_count, 6)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)

    def test_action_not_permitted_on_unavailable_instances(self):
        """
        An action instance cannot be started if the patient instance is dead or a lab is not available
        """
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.patient_instance.patient_state.is_dead = True
        action_instance.patient_instance.patient_state.save(update_fields=["is_dead"])
        succeeded, _ = action_instance.try_application()
        self.assertFalse(succeeded)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)


class ActionInstanceScheduledTestCase(TestUtilsMixin, TestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.deactivate_notifications()
        self.deactivate_results()

        self.action_instance = ActionInstanceFactory(patient_instance=PatientFactory())
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)

    def tearDown(self):
        self.activate_notifications()
        self.activate_results()

        settings.CURRENT_TIME = self.variable_backup

    def test_action_scheduling(self):
        """
        Iff running, an action has a corresponding scheduled event.
        Once it stopped running, it changes it's state to finished.
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
