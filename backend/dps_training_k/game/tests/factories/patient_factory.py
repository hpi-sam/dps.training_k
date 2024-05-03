import factory

from game.models import PatientInstance
from template.tests.factories import EmptyPatientStateFactory
from .area_factory import AreaFactory
from .exercise_factory import ExerciseFactory
from .inventory_factory import EmptyInventoryFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientInstance
        django_get_or_create = ("name", "exercise", "patient_id")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    patient_id = 123456
    triage = "R"
    area = factory.SubFactory(AreaFactory)
    patient_state = factory.SubFactory(EmptyPatientStateFactory)

    @factory.post_generation
    def generate_inventory(self, create, extracted, **kwargs):
        if not create:
            return
        EmptyInventoryFactory(patient_instance=self)
