from django.core.management.base import BaseCommand

from configuration import settings
from game.models import Exercise, PatientInstance, Area
from template.models import PatientInformation


class Command(BaseCommand):
    help = "Creates a basic exercise one can join immediately without having to create it via the trainer interface first."

    def handle(self, *args, **options):
        if not Exercise.objects.filter(exercise_frontend_id="abcdef").exists():
            settings.ID_GENERATOR.codes_taken.append("abcdef")
            settings.ID_GENERATOR.codes_taken.append("123456")
        else:
            Exercise.objects.get(exercise_frontend_id="abcdef").delete()

        self.exercise = Exercise.objects.create(
            exercise_frontend_id="abcdef",
            state=Exercise.ExerciseStateTypes.CONFIGURATION,
        )
        self.area = Area.create_area(
            name="Bereich", exercise=self.exercise, isPaused=False
        )
        self.patient_information = PatientInformation.objects.get(code=1004)

        self.patient = PatientInstance.objects.create(
            name="Max Mustermann",
            static_information=self.patient_information,
            exercise=self.exercise,
            area=self.area,
            patient_frontend_id=123456,
        )
        self.stdout.write(
            self.style.SUCCESS("Successfully added debug_exercise to the database")
        )
