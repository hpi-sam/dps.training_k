from django.core.management.base import BaseCommand

from template.constants import (
    ActionIDs,
    MaterialIDs,
    RoleIDs,
    ActionResultIDs,
    role_map,
)
from template.models import Action
import json


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        self.create_actions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added minimal actions to the database")
        )

    @staticmethod
    def create_actions():
        # Treatments
        Action.objects.update_or_create(
            name="i.V. Zugang",
            uuid=ActionIDs.IV_ZUGANG,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    }
                ),
                "results": json.dumps({}),
            },
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt",
            uuid=ActionIDs.VOLLELEKTROLYT,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    }
                ),
                "results": json.dumps({}),
            },
        )
        # Examinations
        Action.objects.update_or_create(
            name="Hämoglobinanalyse",
            uuid=ActionIDs.HAEMOGLOBINANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            [
                                {role_map[RoleIDs.LABORASSISTENT]: 1},
                                {role_map[RoleIDs.ARZT]: 1},
                            ]
                        ],
                    }
                ),
                "results": json.dumps(
                    {
                        "Hb": [
                            {ActionResultIDs.HB420: "Ergebnis1"},
                            {ActionResultIDs.HB430: "Ergebnis2"},
                        ]
                    }
                ),
            },
        )
        # Produce Material
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma (0 positiv) auftauen",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_AUFTAUEN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)],
                        "num_personnel": 0,  # TODo: Add back once personnel for labs is being used
                        "lab_devices": None,
                        "area": None,
                        "role": [],  # TODo: Add back once personnel for labs is being used
                    }
                ),
                "results": json.dumps(
                    {
                        "produced_material": {
                            str(MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS): 1
                        }
                    }
                ),
            },
        )
