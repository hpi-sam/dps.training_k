import factory

from .area_factory import AreaFactory
from game.models import Personnel


class PersonnelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Personnel
        django_get_or_create = ("name", "area", "assigned_patient")

    name = "Maxim Musterfrau"
    area = AreaFactory()
    assigned_patient = None
