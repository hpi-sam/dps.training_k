import factory
from game.models import MaterialInstance
from template.tests.factories import MaterialFactory


class MaterialInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MaterialInstance
        django_get_or_create = [
            "action_instance",
            "area",
            "lab",
            "template",
            "patient_instance",
        ]

    action_instance = None
    area = None
    lab = None
    template = factory.SubFactory(MaterialFactory)
    patient_instance = None
