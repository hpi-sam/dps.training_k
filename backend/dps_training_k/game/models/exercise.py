from django.conf import settings
from django.db import models

from game.channel_notifications import ExerciseDispatcher
from .lab import Lab
from .scheduled_event import ScheduledEvent
from .log_entry import LogEntry


class Exercise(models.Model):
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
        editable=False,
    )
    state = models.CharField(
        choices=StateTypes.choices,
        default=StateTypes.CONFIGURATION,
    )
    trainer = models.ForeignKey(
        to="User",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    @classmethod
    def createExercise(cls, trainer):
        new_Exercise = cls.objects.create(
            frontend_id=settings.ID_GENERATOR.get_exercise_frontend_id(),
            state=cls.StateTypes.CONFIGURATION,
            trainer=trainer,
        )
        Lab.objects.create(exercise=new_Exercise)
        return new_Exercise

    def start_exercise(self):
        from .patient_instance import PatientInstance

        owned_patients = PatientInstance.objects.filter(exercise=self)
        for time_offset, patient in enumerate(owned_patients):
            # we don't start all patients at once to balance out the work for our celery workers
            patient.schedule_state_change(time_offset)
        self.update_state(Exercise.StateTypes.RUNNING)
        for patient in owned_patients:
            patient.apply_pretreatments()

    def save(self, *args, **kwargs):
        changes = kwargs.get("update_fields", None)
        ExerciseDispatcher.save_and_notify(self, changes, super(), *args, **kwargs)

    def update_state(self, state):
        old_state = self.state
        self.state = state
        self.save(update_fields=["state"])
        if not self.is_running_state(old_state) and self.is_running_state(state):
            LogEntry.set_empty_timestamps(self)
        elif self.state == self.StateTypes.FINISHED:
            ScheduledEvent.remove_events_of_exercise(self)

    def time_factor(self):
        # config currently is not being used, but could be implemented as follows:
        # if self.config is None:
        #     return 1
        # return 1 / self.config.time_speed_up
        if settings.DEBUG == True:
            return 0.1
        return 1

    def is_running(self):
        return self.is_running_state(self.state)

    @classmethod
    def is_running_state(cls, state):
        return state == cls.StateTypes.RUNNING

    def __str__(self):
        return f"Exercise {self.frontend_id}"
