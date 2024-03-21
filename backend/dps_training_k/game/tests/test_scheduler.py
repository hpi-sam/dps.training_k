from django.test import TestCase
from django.conf import settings
from game.tests.factories import PatientFactory
from game.models import ScheduledEvent
from django.utils import timezone
from game.tasks import check_for_updates
import datetime
import time


class EventPatientTestCase(TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.patient = PatientFactory()
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)

    def test_event_is_triggered(self):
        # ToDo: adapt to actual method later on
        self.patient.schedule_temporary_event()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(9)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 0)

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
