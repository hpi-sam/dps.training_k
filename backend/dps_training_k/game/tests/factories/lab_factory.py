import factory
from game.models import Lab
from game.tests.factories import ExerciseFactory, FilledInventoryFactory


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lab
        django_get_or_create = ("name", "exercise")

    name = "TestLab"
    exercise = factory.SubFactory(ExerciseFactory)

    @factory.post_generation
    def generate_inventory(self, create, extracted, **kwargs):
        if not create:
            return
        FilledInventoryFactory(area=None, lab=self)
