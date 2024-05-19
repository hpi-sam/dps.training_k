from django.conf import settings
from django.db import models

from game.channel_notifications import ExerciseDispatcher
from helpers.eventable import NonEventable
from .lab import Lab
from .log_entry import LogEntry


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
    frontend_id = models.CharField(
        unique=True,
        editable=settings.DEBUG,
    )
    state = models.CharField(
        choices=StateTypes.choices,
        default=StateTypes.CONFIGURATION,
    )

    @classmethod
    def createExercise(cls):
        new_Exercise = cls.objects.create(
            frontend_id=settings.ID_GENERATOR.get_exercise_frontend_id(),
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
        if not self.is_running_state(old_state) and self.is_running_state(state):
            LogEntry.set_empty_timestamps(self)

    def time_factor(self):
        if self.config is None:
            return 1
        return 1 / self.config.time_speed_up

    def is_running(self):
        return self.is_running_state(self.state)

    @classmethod
    def is_running_state(cls, state):
        if state == cls.StateTypes.RUNNING:
            return True
        return False

    def __str__(self):
        return f"Exercise {self.frontend_id}"
