import factory

from game.models import PatientInstance
from template.tests.factories import EmptyPatientStateFactory
from .area_factory import AreaFactory
from .exercise_factory import ExerciseFactory
from .patient_information_factory import PatientInformationFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientInstance
        django_get_or_create = ("name", "exercise", "frontend_id", "triage", "area", "patient_state", "static_information",)

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    frontend_id = factory.Sequence(lambda n: f'{n:06d}') # generate unique 6 digit frontend_id
    triage = "R"
    area = factory.SubFactory(AreaFactory)
    patient_state = factory.SubFactory(EmptyPatientStateFactory)
    static_information = factory.SubFactory(PatientInformationFactory)
