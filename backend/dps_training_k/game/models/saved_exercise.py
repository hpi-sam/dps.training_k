from django.db import models

from helpers.name_generator import NameGenerator
from .exercise import Exercise
from ..serializers.exercise_serializer import ExerciseSerializer


class SavedExercise(models.Model):
    name = models.CharField(unique=True)
    saved_exercise = models.JSONField()
    time_speed_up = models.FloatField(default=1.0)


class SavedExerciseFactory:
    def __init__(
        self,
        exercise: Exercise,
        exercise_serializer: ExerciseSerializer,
        name_generator: NameGenerator,
    ):
        self.exercise = exercise
        self.exercise_serializer = exercise_serializer
        self.name_generator = name_generator

    def snapshot_exercise(self):
        serialized_exercise = ExerciseSerializer(self.exercise).data
        name = self.name_generator.generate_name()
        return SavedExercise.objects.create(
            saved_exercise=serialized_exercise, name=name
        )
