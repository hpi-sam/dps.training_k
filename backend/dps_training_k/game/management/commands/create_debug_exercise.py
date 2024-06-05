from django.core.management.base import BaseCommand

from configuration import settings
from game.consumers import TrainerConsumer
from game.models import Exercise, PatientInstance, Area, Personnel, User
from template.models import PatientInformation, PatientState


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

        user, created = User.objects.get_or_create(username="test", user_type=User.UserType.TRAINER)
        if not created:
            user.set_password("password")
            user.save()
        self.exercise = Exercise.createExercise(user)
        self.exercise.frontend_id = "abcdef"
        self.area = Area.create_area(
            name="Bereich", exercise=self.exercise, isPaused=False
        )
        self.patient_information = PatientInformation.objects.get(code=1004)
        patient_state = PatientState.objects.get(
            code=self.patient_information.code,
            state_id=self.patient_information.start_status,
        )

        self.patient, _ = PatientInstance.objects.update_or_create(
            frontend_id=123456,
            patient_state=patient_state,
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
                "patient_instance": self.patient,
            },
        )
        Personnel.objects.update_or_create(
            name="Pflegekraft 2",
            defaults={
                "patient_instance": self.patient,
            },
        )

        TrainerConsumer.handle_start_exercise(_, self.exercise)

        self.stdout.write(
            self.style.SUCCESS("Successfully added debug_exercise to the database")
        )
