import factory
from django.conf import settings
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "models"))
from .exercise import Exercise


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise
        django_get_or_create = ("config", "invitation_code", "state")

    config = factory.SubFactory(SavedExerciseFactory)
    invitation_code = "a" * settings.INVITATION_LOGIC.code_length
    state = Exercise.ExerciseStateTypes.CONFIGURATION


class SavedExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavedExercise
        django_get_or_create = ("saved_exercise", "name", "time_speed_up")

    saved_exercise = {}
    name = "TestSavedExercise"
    time_speed_up = 1.0
