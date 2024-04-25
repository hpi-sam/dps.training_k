import factory
from template.models import Resource
from template.constants import MaterialIDs


class ResourceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Resource
        django_get_or_create = ("name", "is_returnable")

    uuid = MaterialIDs.CONCENTRATED_RED_CELLS_0_POS
    name = "Enthrozytenkonzentrat 0 pos."
    is_returnable = False
