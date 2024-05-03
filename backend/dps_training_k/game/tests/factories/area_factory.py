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
    isPaused = False

    @factory.post_generation
    def generate_inventory(self, create, extracted, **kwargs):
        if not create:
            return
        EmptyInventoryFactory(area=self)
