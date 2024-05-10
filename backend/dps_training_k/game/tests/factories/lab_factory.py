import factory
from game.models import Lab
from .exercise_factory import ExerciseFactory


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lab
        django_get_or_create = ("exercise",)

    exercise = factory.SubFactory(ExerciseFactory)
