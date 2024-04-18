from django.test import TestCase
from django.conf import settings
from game.tests.factories import PatientFactory
from game.models import ScheduledEvent
from django.utils import timezone
from game.tasks import check_for_updates
from unittest.mock import patch
import datetime


class EventPatientTestCase(TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.patient_instance = PatientFactory()
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)
        ScheduledEvent.create_event(
            self.patient_instance.exercise,
            10,
            "execute_state_change",
            patient=self.patient_instance,
        )

    @patch("game.models.PatientInstance.execute_state_change")
    def test_scheduler_is_triggered(self, execute_state_change):
        """
        Scheduler only triggers for times bigger or equal to the scheduled time.
        """
        execute_state_change.return_value = True
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(9)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 0)

    @patch("game.models.PatientInstance.execute_state_change")
    def test_event_is_triggered(self, execute_state_change):
        """
        The action method of the scheduler is able to dispatch the specified method of the related instance.
        """
        execute_state_change.return_value = True
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        self.assertEqual(execute_state_change.call_count, 1)

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
