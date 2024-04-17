from django.core.management.base import BaseCommand
from template.models import Action


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        self.create_actions()
        self.stdout.write(self.style.SUCCESS("Successfully added data to the database"))

    @staticmethod
    def create_actions():
        # Treatments
        Action.objects.update_or_create(
            name="i.V. Zugang",
            category="TR",
            application_duration=60,
            effect_duration=120,  # depends on type of "Zugang"
            conditions={"Personnel": 1, "Role": "Pflegefachkraft"},
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt 1000ml",
            category="TR",
            application_duration=0,  # depends on type of "Zugang"
            effect_duration=120,
            conditions={
                "Personnel": 1,
                "Role": "Pflegefachkraft",
                "Actions_required": "i.V. Zugang",
            },
        )
        # Examinations
        Action.objects.update_or_create(
            name="EKG anbringen",
            category="EX",
            application_duration=60,  # depends on type of "Zugang"
            effect_duration=None,  # None means permanent
            conditions={"Personnel": 1, "Role": "Pflegefachkraft"},
        )
