import factory

from game.models import Personnel


class PersonnelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Personnel
        django_get_or_create = ("name", "area", "patient_instance")

    name = "Maxim Musterfrau"
    area = None
    patient_instance = None
