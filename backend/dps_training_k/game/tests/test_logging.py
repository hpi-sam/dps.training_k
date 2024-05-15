from django.test import TestCase
from unittest.mock import patch
from game.models import LogEntry, Exercise
from .factories import ExerciseFactory


class TrainerLogTestCase(TestCase):
    def setUp(self):
        self.exercise = ExerciseFactory()
        self.log_entry, _ = LogEntry.objects.get_or_create(
            exercise=self.exercise, message="Test 1"
        )

    @patch("game.channel_notifications.LogEntryDispatcher._notify_log_update_event")
    def test_logs_held_back_on_inactive_exercise(self, _notify_log_update_event):
        """
        When an exercise is not RUNNING, the log entries are invalid. Invalid log entries are not sent to the frontend.
        """
        self.assertEqual(self.log_entry.timestamp, None)
        self.assertEqual(self.log_entry.is_valid(), False)
        self.assertEqual(_notify_log_update_event.call_count, 0)

    @patch("game.channel_notifications.LogEntryDispatcher._notify_log_update_event")
    def test_logs_timestamped_on_active_exercise(self, _notify_log_update_event):
        """
        When an exercise enters the running state, all invalid log_entries are timestamped and sent to the frontend.
        New log entries are timestamped and sent to the frontend directly.
        """
        self.exercise.update_state(Exercise.StateTypes.RUNNING)
        log_entries = LogEntry.objects.filter(exercise=self.exercise)
        for log_entry in log_entries:
            self.assertNotEqual(log_entry.timestamp, None)
            self.assertEqual(log_entry.is_valid(), True)
        self.assertEqual(_notify_log_update_event.call_count, log_entries.count())

        self.log_entry = LogEntry.objects.create(
            exercise=self.exercise, message="Test 2"
        )
        self.assertNotEqual(self.log_entry.timestamp, None)
        self.assertEqual(self.log_entry.is_valid(), True)
        self.assertEqual(
            _notify_log_update_event.call_count,
            LogEntry.objects.filter(exercise=self.exercise).count(),
        )
