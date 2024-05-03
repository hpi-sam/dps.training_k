import factory
from game.models import Lab
from game.tests.factories import ExerciseFactory, EmptyInventoryFactory


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lab
        django_get_or_create = ("name", "exercise")

    name = "TestLab"
    exercise = factory.SubFactory(ExerciseFactory)
    inventory = factory.SubFactory(EmptyInventoryFactory)
