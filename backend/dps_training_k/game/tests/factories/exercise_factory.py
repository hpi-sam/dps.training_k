import factory
from django.conf import settings

from game.models import Exercise, SavedExercise


class SavedExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavedExercise
        django_get_or_create = ("saved_exercise", "name", "time_speed_up")

    saved_exercise = {}
    name = "TestSavedExercise"
    time_speed_up = 1.0


class ExerciseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Exercise
        django_get_or_create = ("config", "frontend_id", "state")

    config = factory.SubFactory(SavedExerciseFactory)
    frontend_id = "a" * settings.ID_GENERATOR.code_length
    state = Exercise.StateTypes.CONFIGURATION
