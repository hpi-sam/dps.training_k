from django.db import models
from django.utils import timezone

from game.channel_notifications import LogEntryDispatcher


class LogEntry(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["local_id", "exercise"], name="unique_local_id_for_entry"
            )
        ]

    local_id = models.IntegerField(blank=True)
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(
        null=True, blank=True, help_text="May only be set while exercise is running"
    )
    message = models.TextField()
    is_dirty = models.BooleanField(
        default=False,
        help_text="Set to True if objects is missing relevant Keys (e.g. timestamp)",
    )

    patient_instance = models.ForeignKey(
        "PatientInstance", on_delete=models.CASCADE, null=True, blank=True
    )
    area = models.ForeignKey("Area", on_delete=models.CASCADE, null=True, blank=True)
    materials = models.ManyToManyField("MaterialInstance", blank=True)
    personnel = models.ManyToManyField("Personnel", blank=True)

    def save(self, *args, **kwargs):
        if self._state.adding:
            if self.exercise.is_running():
                self.timestamp = timezone.now()
            else:
                self.timestamp = None

            self.local_id = self.generate_local_id(
                self.exercise
            )  # prone to race conditions

        changes = kwargs.get("update_fields", None)
        LogEntryDispatcher.save_and_notify(self, changes, super(), *args, **kwargs)

    @classmethod
    def set_empty_timestamps(cls, exercise):
        log_entries = cls.objects.filter(exercise=exercise, timestamp=None)
        current_timestamp = timezone.now()
        for log_entry in log_entries:
            log_entry.timestamp = current_timestamp
            log_entry.save(update_fields=["timestamp"])
        return log_entries

    def generate_local_id(self, exercise):
        highest_local_id = LogEntry.objects.filter(exercise=exercise).aggregate(models.Max("local_id"))["local_id__max"]
        if highest_local_id:
            return highest_local_id + 1
        return 1

    def is_valid(self):
        if self.timestamp and self.local_id and not self.is_dirty:
            return True
        return False

    def set_dirty(self, new_dirty):
        self.is_dirty = new_dirty
        self.save(update_fields=["is_dirty"])
