import json

from django.core.management.base import BaseCommand

from template.constants import (
    ActionIDs,
    MaterialIDs,
    RoleIDs,
    role_map,
)
from template.models import Action


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        self.create_actions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added minimal action list to the database")
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
                "application_duration": 5,
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
                "application_duration": 10,  # For debugging purposes
                "effect_duration": None,
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
                                {role_map[RoleIDs.ARZT]: 1},
                                {role_map[RoleIDs.LABORASSISTENT]: 1},
                            ],
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Hb": {
                            400: 9.5,
                            401: 12,
                            402: 16,
                            403: 11,
                            404: 5.5,
                            405: 13,
                            406: 7.5,
                            407: 6,
                            408: 9,
                            409: 3.5,
                            410: 3,
                            411: 13,
                            412: 17,
                            413: 8,
                            414: 2.5,
                            415: 8.5,
                            416: 17,
                            417: 6.5,
                            418: 12,
                            419: 7,
                            420: 11,
                            421: 14,
                            422: 10,
                            423: 15,
                            424: 16,
                            425: 4,
                            426: 2,
                            427: 15,
                            428: 5,
                            429: 4.5,
                            430: 14,
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutgruppe bestimmen",
            uuid=ActionIDs.BLUTGRUPPE_BESTIMMEN,
            defaults={
                "category": "EX",
                "application_duration": 10,  # For debugging purposes
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Blutgruppe": {
                            1: "A Rh pos",
                            2: "B Rh pos",
                            3: "A rh neg",
                            4: "0 Rh pos",
                            5: "B rh neg",
                            6: "AB rh neg",
                            7: "O rh neg",
                            8: "AB Rh pos",
                        }
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
