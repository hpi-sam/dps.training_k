import factory
from game.models import Area
from .exercise_factory import ExerciseFactory
from .inventory_factory import EmptyInventoryFactory


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area
        django_get_or_create = ("name", "exercise", "isPaused")

    name = "TestArea"
    exercise = factory.SubFactory(ExerciseFactory)
    inventory = factory.SubFactory(EmptyInventoryFactory)
    isPaused = False
