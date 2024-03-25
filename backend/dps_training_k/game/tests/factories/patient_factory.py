import factory
from .exercise_factory import ExerciseFactory
from game.models import Patient


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient
        django_get_or_create = ("name", "exercise", "patientId")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    patientId = 123456
