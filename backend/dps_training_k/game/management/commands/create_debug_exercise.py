from django.core.management.base import BaseCommand

from configuration import settings
from game.consumers import TrainerConsumer
from game.models import Exercise, PatientInstance, Area, Personnel
from template.models import PatientInformation


class Command(BaseCommand):
    help = "Creates a basic exercise one can join immediately without having to create it via the trainer interface first."

    def handle(self, *args, **options):
        if not Exercise.objects.filter(frontend_id="abcdef").exists():
            settings.ID_GENERATOR.codes_taken.append("abcdef")
        else:
            Exercise.objects.get(frontend_id="abcdef").delete()

        # I have no friggin idea why this is necessary, but it is (exercise deletion should cascade area and therefore patient deletion)
        if not PatientInstance.objects.filter(frontend_id=123456).exists():
            settings.ID_GENERATOR.codes_taken.append("123456")
        else:
            PatientInstance.objects.get(frontend_id=123456).delete()

        self.exercise = Exercise.createExercise()
        self.exercise.frontend_id = "abcdef"
        self.area = Area.create_area(
            name="Bereich", exercise=self.exercise, isPaused=False
        )
        self.patient_information = PatientInformation.objects.get(code=1004)

        self.patient, _ = PatientInstance.objects.update_or_create(
            frontend_id=123456,
            defaults={
                "name": "Max Mustermann",
                "static_information": self.patient_information,
                "exercise": self.exercise,
                "area": self.area,
            },
        )
        Personnel.objects.update_or_create(
            name="Pflegekraft 1",
            defaults={
                "area": self.area,
                "assigned_patient": self.patient,
            },
        )
        Personnel.objects.update_or_create(
            name="Pflegekraft 2",
            defaults={
                "area": self.area,
                "assigned_patient": self.patient,
            },
        )

        TrainerConsumer.handle_start_exercise(_, self.exercise)

        self.stdout.write(
            self.style.SUCCESS("Successfully added debug_exercise to the database")
        )
