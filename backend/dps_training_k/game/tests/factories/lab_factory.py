import factory
from game.models import Lab
from game.tests.factories import ExerciseFactory


class LabFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lab
        django_get_or_create = ("name", "exercise")

    name = "TestLab"
    exercise = factory.SubFactory(ExerciseFactory)

    @factory.post_generation
    def generate_inventory(self, create, extracted, **kwargs):
        from game.tests.factories import EmptyInventoryFactory

        if not create:
            return
        EmptyInventoryFactory(lab=self)
