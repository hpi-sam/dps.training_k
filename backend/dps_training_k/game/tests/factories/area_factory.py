import factory
from game.models import Area
from .exercise_factory import ExerciseFactory


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area
        django_get_or_create = ("name", "exercise", "isPaused")

    name = "TestArea"
    exercise = factory.SubFactory(ExerciseFactory)
    isPaused = False
