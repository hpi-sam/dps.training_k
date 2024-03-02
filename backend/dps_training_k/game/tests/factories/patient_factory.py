import factory
from .exercise_factory import ExerciseFactory


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Patient
        django_get_or_create = ("name", "exercise", "patientCode")

    name = "Max Mustermann"
    exercise = factory.SubFactory(ExerciseFactory)
    patientCode = 123456
