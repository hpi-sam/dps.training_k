import factory

from game.models import Personnel
from .area_factory import AreaFactory


class PersonnelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Personnel
        django_get_or_create = ("name", "area", "patient_instance")

    name = "Maxim Musterfrau"
    area = factory.SubFactory(AreaFactory)
    patient_instance = None
