from django.conf import settings
from django.db import models
from .log_entry import LogEntry
from .lab import Lab
from helpers.eventable import NonEventable
from game.channel_notifications import ExerciseDispatcher


class Exercise(NonEventable, models.Model):
    class StateTypes(models.TextChoices):
        CONFIGURATION = "C", "configuration"
        RUNNING = "R", "running"
        PAUSED = "P", "paused"
        FINISHED = "F", "finished"

    config = models.ForeignKey(
        to="SavedExercise",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    exercise_frontend_id = models.CharField(
        unique=True,
        editable=settings.DEBUG,
    )
    state = models.CharField(
        choices=StateTypes.choices,
        default=StateTypes.CONFIGURATION,
    )
    """trainer = models.ForeignKey(
        to="Trainer",
        on_delete=models.CASCADE,
    ) """

    @classmethod
    def createExercise(cls):
        new_Exercise = cls.objects.create(
            exercise_frontend_id=settings.ID_GENERATOR.get_exercise_frontend_id(),
            state=cls.StateTypes.CONFIGURATION,
        )
        Lab.objects.create(exercise=new_Exercise)
        return new_Exercise

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ExerciseDispatcher.save_and_notify(self, changes, super(), *args, **kwargs)

    def update_state(self, state):
        old_state = self.state
        self.state = state
        self.save(update_fields=["state"])
        if old_state != self.StateTypes.RUNNING and state == self.StateTypes.RUNNING:
            LogEntry.set_empty_timestamps(self)

    def time_factor(self):
        if self.config is None:
            return 1
        return 1 / self.config.time_speed_up

    def is_running(self):
        if self.state == self.StateTypes.RUNNING:
            return True
        return False
