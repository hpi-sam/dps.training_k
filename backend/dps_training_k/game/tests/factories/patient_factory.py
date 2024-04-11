import factory

from game.models import Patient
from template.tests.factories import EmptyPatientStateFactory
from .area_factory import AreaFactory
from .exercise_factory import ExerciseFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient
        django_get_or_create = ("name", "exercise", "patientId")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    patientId = 123456
    triage = "R"
    area = factory.SubFactory(AreaFactory)
    patient_state = factory.SubFactory(EmptyPatientStateFactory)
