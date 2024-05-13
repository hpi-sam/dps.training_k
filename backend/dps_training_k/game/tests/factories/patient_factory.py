import factory

from game.models import PatientInstance
from template.tests.factories import EmptyPatientStateFactory
from .area_factory import AreaFactory
from .exercise_factory import ExerciseFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientInstance
        django_get_or_create = ("name", "exercise", "frontend_id")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    frontend_id = 123456
    triage = "R"
    area = factory.SubFactory(AreaFactory)
    patient_state = factory.SubFactory(EmptyPatientStateFactory)
