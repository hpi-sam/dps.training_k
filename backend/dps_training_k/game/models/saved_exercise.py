from django.db import models

from .exercise import Exercise
from helpers.name_generator import NameGenerator, DateTimeNameGenerator
from helpers.exercise_serializer import ExerciseSerializer


class SavedExercise(models.Model):
    saved_exercise = models.JSONField()
    name = models.CharField(unique=True)

    @classmethod
    def save_exercise(cls, serialized_exercise, name):
        return cls.objects.create(serialized_exercise, name)


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
        serialized_exercise = self.exercise_serializer.serialize(self.exercise)
        name = self.name_generator.generate_name()
        return SavedExercise.save_exercise(serialized_exercise, name)
