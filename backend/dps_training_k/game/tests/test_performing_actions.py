from django.test import TestCase
from django.conf import settings
from game.models import ScheduledEvent, ActionInstance, ActionInstanceStateNames
from game.tasks import check_for_updates
from .factories import PatientFactory, ActionInstanceFactory
from template.tests.factories import ActionFactory
from unittest.mock import patch
from django.utils import timezone
import datetime


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
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.DECLINED)

    def test_action_starting(self):
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
        self.application_status.return_value = True, None
        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        action_instance.try_application()
        self.assertEqual(_notify_action_event.call_count, 1)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )

        action_instance = ActionInstance.create(ActionFactory(), PatientFactory())
        self.application_status.return_value = False, "Not applicable"
        action_instance.try_application()
        self.assertEqual(_notify_action_event.call_count, 2)
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.ON_HOLD)


class ActionInstanceScheduledTestCase(TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.action_instance = ActionInstanceFactory()
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup

    def test_action_is_scheduled(self):
        self.action_instance._start_application()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 0)
        self.action_instance.refresh_from_db()  # Warning: Not working without, although it should.
        # ToDo: Find out why this is necessary at this test and not on the other ones
        self.assertEqual(
            self.action_instance.current_state.name, ActionInstanceStateNames.FINISHED
        )
