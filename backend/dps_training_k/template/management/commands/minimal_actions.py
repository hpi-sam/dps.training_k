from django.core.management.base import BaseCommand
from template.models import Action
from template.constants import ActionIDs, MaterialIDs, RoleIDs, role_map


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
                    "material": {MaterialIDs.IV_ZUGANG: 1},
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
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
                    "required_actions": [ActionIDs.IV_Zugang],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                },
            },
        )
        # Examinations
        Action.objects.update_or_create(
            name="Hämoglobinanalyse",
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,  # None means permanent
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [[{role_map[RoleIDs.LABORASSISTENT]: 1}, {role_map[RoleIDs.ARZT]}]],
                },
            },
        )
