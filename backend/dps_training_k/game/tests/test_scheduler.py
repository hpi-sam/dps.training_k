from django.test import TestCase
from django.conf import settings
from game.tests.factories import PatientFactory
from game.models import Patient, ScheduledEvent
from django.utils import timezone
from game.tasks import check_for_updates
import datetime
import logging

logger = logging.getLogger(__name__)


class TempEventTest:
    def schedule_temporary_event(self):
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "temporary_event_test",
            patient=self,
        )

    def temporary_event_test(self):
        return True


class EventPatientTestCase(TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.patient = PatientFactory()
        # ToDo: get to work
        """self.patient.schedule_temporary_event = (
            TempEventTest.schedule_temporary_event.__get__(self.patient)
        )
        self.patient.schedule_temporary_event = (
            TempEventTest.temporary_event_test.__get__(self.patient)
        )"""
        self.cache = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)

    def test_event_is_triggered(self):
        self.patient.schedule_temporary_event()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        # ToDo: Adapt in case celery beat is running in parallel
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(9)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        self.assertEqual(ScheduledEvent.objects.count(), 0)

    def tearDown(self):
        settings.CURRENT_TIME = self.cache
