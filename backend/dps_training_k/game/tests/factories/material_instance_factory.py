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
            "material_template",
            "patient_instance",
        ]

    action_instance = None
    area = None
    lab = None
    material_template = factory.SubFactory(MaterialFactory)
    patient_instance = None
