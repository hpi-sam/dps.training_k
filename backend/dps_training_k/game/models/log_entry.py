from django.db import models
from game.channel_notifications import LogEntryDispatcher
import datetime


class LogEntry(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["local_id", "exercise"], name="unique_local_id_for_entry"
            )
        ]

    local_id = models.IntegerField()
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        null=True, blank=True, help_text="May only be set while exercise is running"
    )
    message = models.TextField()
    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True, blank=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True, blank=True)
    personnel = models.ForeignKey(
        "Personnel", on_delete=models.CASCADE, null=True, blank=True
    )
    # lab = models.ForeignKey("Lab", on_delete=models.CASCADE, null=True, blank=True) ToDo: Uncomment when Lab model is implemented

    def save(self, *args, **kwargs):
        if self._state.adding and not self.exercise.is_running():
            self.timestamp = None
        changes = kwargs.get("update_fields", None)
        LogEntryDispatcher.save_and_notify(self, changes, *args, **kwargs)

    @classmethod
    def set_empty_timestamps(cls, exercise):
        log_entries = cls.objects.filter(exercise=exercise)
        current_timestamp = datetime.datetime.now()
        for log_entry in log_entries:
            log_entry.timestamp = current_timestamp
            log_entry.save(update_fields=["timestamp"])
        return log_entries

    def is_valid(self):
        if self.timestamp:
            return True
        return False
