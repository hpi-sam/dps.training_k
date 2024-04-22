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
        django_get_or_create = ("config", "exercise_frontend_id", "state")

    config = factory.SubFactory(SavedExerciseFactory)
    exercise_frontend_id = "a" * settings.INVITATION_LOGIC.code_length
    state = Exercise.ExerciseStateTypes.CONFIGURATION
