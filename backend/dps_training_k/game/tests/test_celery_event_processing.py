import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import timezone

from game.models import ScheduledEvent
from game.tasks import check_for_updates, run_event
from game.tests.factories import PatientFactory


class CeleryEventProcessingTestCase(TestCase):
    """Tests that the check_for_updates → run_event pipeline correctly processes
    multiple events via Celery's task queue."""

    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    @patch("game.models.PatientInstance.execute_state_change")
    def test_multiple_events_all_processed(self, execute_state_change):
        """All due events are claimed, enqueued, and executed in a single check_for_updates call."""
        execute_state_change.return_value = True
        num_patients = 20

        patients = [
            PatientFactory(
                name=f"Patient {i}",
                frontend_id=f"{i:06d}",
            )
            for i in range(num_patients)
        ]

        for patient in patients:
            ScheduledEvent.create_event(
                patient.exercise,
                10,
                "execute_state_change",
                patient=patient,
            )

        self.assertEqual(ScheduledEvent.objects.count(), num_patients)

        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(10)
        check_for_updates()

        self.assertEqual(ScheduledEvent.objects.count(), 0)
        self.assertEqual(execute_state_change.call_count, num_patients)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=True)
    @patch("game.models.PatientInstance.execute_state_change")
    def test_enqueued_events_not_claimed_again(self, execute_state_change):
        """Events marked as enqueued are skipped by subsequent check_for_updates calls."""
        execute_state_change.return_value = True

        patient = PatientFactory()
        ScheduledEvent.create_event(
            patient.exercise,
            10,
            "execute_state_change",
            patient=patient,
        )

        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(10)

        # First call processes the event
        check_for_updates()
        self.assertEqual(execute_state_change.call_count, 1)
        self.assertEqual(ScheduledEvent.objects.count(), 0)

        # Create a new event and manually mark it enqueued (simulating in-flight task)
        ScheduledEvent.create_event(
            patient.exercise,
            10,
            "execute_state_change",
            patient=patient,
        )
        ScheduledEvent.objects.update(enqueued=True)

        # Second call should skip the already-enqueued event
        check_for_updates()
        self.assertEqual(execute_state_change.call_count, 1)

    @override_settings(
        CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPAGATES=False
    )
    def test_failed_event_deleted_after_max_retries(self):
        """An event pointing to a nonexistent method is deleted after exhausting retries.
        Uses .apply() so Celery's eager retry machinery properly increments the retry counter.
        EAGER_PROPAGATES must be False so self.retry() re-executes inline instead of re-raising.
        """
        patient = PatientFactory()
        ScheduledEvent.create_event(
            patient.exercise,
            10,
            "nonexistent_method",
            patient=patient,
        )
        self.assertEqual(ScheduledEvent.objects.count(), 1)

        event_id = ScheduledEvent.objects.first().id
        run_event.apply(args=[event_id])

        self.assertEqual(ScheduledEvent.objects.count(), 0)
