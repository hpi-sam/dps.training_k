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
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": {"i.V. Zugang": 1},
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": {"Pflegefachkraft": 1},
                },
            },
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt 1000ml",
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": {
                    "required_actions": ["i.V. Zugang"],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": {"Pflegefachkraft": 1},
                },
            },
        )
        # Examinations
        Action.objects.update_or_create(
            name="EKG anbringen",
            defaults={
                "category": "EX",
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": {"Pflegefachkraft": 1},
                },
            },
        )
