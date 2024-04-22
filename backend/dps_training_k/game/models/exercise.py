from django.conf import settings
from django.db import models

from helpers.eventable import NonEventable


class Exercise(NonEventable, models.Model):
    class ExerciseStateTypes(models.TextChoices):
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
    """trainer = models.ForeignKey(
        to="Trainer",
        on_delete=models.CASCADE,
    ) """
    exerciseId = models.CharField(
        unique=True,
        editable=settings.DEBUG,
        max_length=settings.INVITATION_LOGIC.code_length,
    )
    state = models.CharField(
        choices=ExerciseStateTypes.choices,
        default=ExerciseStateTypes.CONFIGURATION,
    )

    @classmethod
    def createExercise(cls):
        new_Exercise = cls.objects.create(
            # config=settings.DEFAULT_EXCERCISE_CONFIG,
            # trainer=trainer
            exerciseId=settings.INVITATION_LOGIC.get_exerciseId(),
            state=cls.ExerciseStateTypes.CONFIGURATION,
        )
        return new_Exercise

    def time_factor(self):
        if self.config is None:
            return 1
        return 1 / self.config.time_speed_up

    def serialize(self):
        from game.models import Area

        return {
            "exerciseId": self.exerciseId,
            "areas": [area.serialize() for area in Area.objects.filter(exercise=self)],
        }
