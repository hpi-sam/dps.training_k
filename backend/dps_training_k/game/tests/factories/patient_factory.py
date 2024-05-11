import factory

from game.models import PatientInstance
from template.tests.factories import EmptyPatientStateFactory
from .area_factory import AreaFactory
from .exercise_factory import ExerciseFactory
from .patient_information_factory import PatientInformationFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientInstance
        django_get_or_create = ("name", "exercise", "patient_frontend_id")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    patient_frontend_id = 123456
    triage = "R"
    area = factory.SubFactory(AreaFactory)
    patient_state = factory.SubFactory(EmptyPatientStateFactory)
    static_information = factory.SubFactory(PatientInformationFactory)
