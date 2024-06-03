import json

from django.core.management.base import BaseCommand

from template.constants import ActionIDs, MaterialIDs, RoleIDs, role_map
from template.models import Action


class Command(BaseCommand):
    help = "Populates the database with minimal action list"

    def handle(self, *args, **kwargs):
        self.create_actions()
        self.stdout.write(
            self.style.SUCCESS("Successfully added actions to the database")
        )

    @staticmethod
    def create_actions():
        """
        "category": Action.Category.TREATMENT, // category as defined in Action, short form
        "location": BE, : 60, // application duration in seconds
        "effect_duration": 60,  // effect duration in seconds; None means permanent
        "conditions": {
            "required_actions": ["A1uuid", "A2uuid", ["A3uuid", "A4uuid"]], // this means action1 AND action2 AND (action3 OR action4); can be None
            "prohibitive_actions": ["A1uuid", "A2uuid", ["A3uuid", "A4uuid"]], // this means action1 AND action2 AND (action3 OR action4); can be None
            "material": ["M1uuid", "M2uuid", ["M3uuid", "M4uuid"]], // material1 AND material2 AND (material3 OR material4); can be None
            "num_personnel": 3, // number of personnel required, must be specified -> CANNOT be None
            "lab_devices": ["L1uuid", "L2uuid", ["L3uuid", "L4uuid"]], // labdev1 AND labdev2 AND (labdev3 OR labdev4); can be None
            "area": "ZNA", // area patient has to be in for action to be applicable; can be None
            "role": [{"Pflegefachkraft": 1}, [{"Arzt": 1}, {"Laborassistent": 1}]] // this means 1 Pflegefachkraft AND (1 Arzt OR 1 Laborassistent); CANNOT be None
        'results': {
            "produced_material": {uuid, amount}
            "ZVD": {code: value} //for every possible examination
        }
        }
        """

        Action.objects.update_or_create(
            name="Thoraxdrainage",
            uuid=ActionIDs.THORAXDRAINAGE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 300,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Pleurapunktion",
            uuid=ActionIDs.PLEURAPUNKTION,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Trachealtubus",
            uuid=ActionIDs.TRACHEALTUBUS,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BEATMUNGSBEUTEL)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Larynxmaske",
            uuid=ActionIDs.LARYNXMASKE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BEATMUNGSBEUTEL)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Larynxtubus",
            uuid=ActionIDs.LARYNXTUBUS,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BEATMUNGSBEUTEL)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Guedeltubus",
            uuid=ActionIDs.GUEDELTUBUS,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Wendeltubus",
            uuid=ActionIDs.WENDELTUBUS,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Koniotomietubus",
            uuid=ActionIDs.KONIOTOMIETUBUS,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 180,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.IV_ZUGANG), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 3,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 2},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Analgetikum",
            uuid=ActionIDs.ANALGETIKUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 600,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.ZVK)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Antiasthmatikum",
            uuid=ActionIDs.ANTIASTHMATIKUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 600,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": None,  # Vernebler oder Inhalator
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Kortikosteroid",
            uuid=ActionIDs.KORTIKOSTEROID,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 1800,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Nitrat",
            uuid=ActionIDs.NITRAT,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 600,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Diuretikum",
            uuid=ActionIDs.DIURETIKUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 1200,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Katecholamin",
            uuid=ActionIDs.KATECHOLAMIN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 60,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.IV_ZUGANG), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.SPRITZENPUMPE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Sedativum",
            uuid=ActionIDs.SEDATIVUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 600,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Regional-Narkotikum",
            uuid=ActionIDs.REGIONAL_NARKOTIKUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # "Freifeld", dunno how do handle that
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,  # Spritze und S.C. Kanüle?
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Tetanusprophylaxe",
            uuid=ActionIDs.TETANUSPROPHYLAXE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,  # Spritze und I.M. Kanüle?
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Antikoagulanz",
            uuid=ActionIDs.ANTIKOAGULANZ,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="(Voll-)Narkotikum",
            uuid=ActionIDs.NARKOTIKUM,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # None means permanent
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.NARKOSEGERAET)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt",
            uuid=ActionIDs.VOLLELEKTROLYT,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,  # Depends of type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Plasmaexpander",
            uuid=ActionIDs.PLASMAEXPANDER,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 120,  # Depends of type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="i.V. Zugang",
            uuid=ActionIDs.IV_ZUGANG,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
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
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="ZVK",
            uuid=ActionIDs.ZVK,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 300,
                "effect_duration": 360,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Schleuse",
            uuid=ActionIDs.SCHLEUSE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 240,
                "effect_duration": 60,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="art. Kanüle",
            uuid=ActionIDs.ART_KANUELE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 120,
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
            },
        )
        Action.objects.update_or_create(
            name="mehrlumen ZVK",
            uuid=ActionIDs.MEHRLUMEN_ZVK,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 240,
                "effect_duration": 420,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Regional-Narkose",
            uuid=ActionIDs.REGIONAL_NARKOSE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,  # abhängig von Medikament
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Druckverband",
            uuid=ActionIDs.DRUCKVERBAND,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Turniquet",
            uuid=ActionIDs.TURNIQUET,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Wundversorgung",
            uuid=ActionIDs.WUNDVERSORGUNG,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="chir. Blutstillung",
            uuid=ActionIDs.CHIR_BLUTSTILLUNG,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 180,
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
            },
        )
        Action.objects.update_or_create(
            name="Stifneck",
            uuid=ActionIDs.STIFNECK,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 2},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Vakuumschiene",
            uuid=ActionIDs.VAKUUMSCHIENE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 2},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Beckenschlinge",
            uuid=ActionIDs.BECKENSCHLINGE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 2},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Gipsverband",
            uuid=ActionIDs.GIPSVERBAND,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 300,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Stabile Seitenlage",
            uuid=ActionIDs.STABILE_SEITENLAGE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Schocklage",
            uuid=ActionIDs.SCHOCKLAGE,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Defi + transcutaner Pacer",
            uuid=ActionIDs.DEFI_TRANSCUTANER_PACER,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.IV_ZUGANG),
                            [str(ActionIDs.NARKOTIKUM), str(ActionIDs.ANALGETIKUM)],
                        ],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.DEFI_TRANSCUTANER_PACER)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Beatmungsgerät anbringen",
            uuid=ActionIDs.BEATMUNGSGERAET_ANBRINGEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [
                                str(ActionIDs.TRACHEALTUBUS),
                                str(ActionIDs.LARYNXTUBUS),
                                str(ActionIDs.LARYNXMASKE),
                            ],
                        ],
                        "prohibitive_actions": None,
                        "material": [
                            [
                                str(MaterialIDs.BEATMUNGSGERAET_STATIONAER),
                                str(MaterialIDs.BEATMUNGSGERAET_TRAGBAR),
                            ]
                        ],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Sauerstoff anbringen",
            uuid=ActionIDs.SAUERSTOFF_ANBRINGEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [
                            [
                                str(MaterialIDs.SAUERSTOFF_TRAGBAR),
                                str(MaterialIDs.SAUERSTOFF_STATIONAER),
                            ]
                        ],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutdruck messen",
            uuid=ActionIDs.BLUTDRUCK_MESSEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Blutdruck": {
                            400: "140/90",
                            401: "150/90",
                            402: "100/40",
                            403: "90/50",
                            404: "80/50",
                            405: "100/60",
                            406: "110/60",
                            407: "100/50",
                            408: "130/90",
                            409: "80/35",
                            410: "100/45",
                            411: "150/85",
                            412: "220/125",
                            413: "120/50",
                            414: "170/100",
                            415: "80/65",
                            416: "180/105",
                            417: "130/60",
                            418: "170/70",
                            419: "180/85",
                            420: "200/90",
                            421: "180/90",
                            422: "200/105",
                            423: "80/55",
                            424: "80/40",
                            425: "210/120",
                            426: "170/75",
                            427: "150/75",
                            428: "70/50",
                            429: "140/100",
                            430: "110/80",
                            431: "140/75",
                            432: "120/55",
                            433: "60/45",
                            434: "160/80",
                            435: "100/80",
                            436: "180/95",
                            437: "160/110",
                            438: "180/75",
                            439: "140/80",
                            440: "210/115",
                            441: "220/100",
                            442: "70/40",
                            443: "100/75",
                            444: "170/85",
                            445: "110/45",
                            446: "120/80",
                            447: "70/55",
                            448: "150/95",
                            449: "150/80",
                            450: "60/40",
                            451: "100/65",
                            452: "210/110",
                            453: "120/70",
                            454: "200/110",
                            455: "110/50",
                            456: "140/85",
                            457: "170/90",
                            458: "190/90",
                            459: "160/100",
                            460: "210/80",
                            461: "160/85",
                            462: "130/65",
                            463: "90/40",
                            464: "80/60",
                            465: "160/75",
                            466: "190/80",
                            467: "140/65",
                            468: "220/95",
                            469: "200/95",
                            470: "150/70",
                            471: "190/85",
                            472: "90/75",
                            473: "90/60",
                            474: "90/45",
                            475: "110/85",
                            476: "190/75",
                            477: "100/70",
                            478: "170/95",
                            479: "n.m.",
                            480: "130/75",
                            481: "190/100",
                            482: "210/100",
                            483: "220/105",
                            484: "110/55",
                            485: "90/65",
                            486: "220/90",
                            487: "160/95",
                            488: "220/115",
                            489: "170/110",
                            490: "200/80",
                            491: "200/100",
                            492: "140/70",
                            493: "210/95",
                            494: "150/65",
                            495: "170/105",
                            496: "110/70",
                            497: "70/45",
                            498: "170/80",
                            499: "150/100",
                            500: "210/85",
                            501: "190/105",
                            502: "120/60",
                            503: "180/70",
                            504: "80/45",
                            505: "210/90",
                            506: "130/85",
                            507: "200/120",
                            508: "140/60",
                            509: "100/55",
                            510: "140/95",
                            511: "60/50",
                            512: "180/110",
                            513: "190/110",
                            514: "210/105",
                            515: "90/55",
                            516: "120/90",
                            517: "160/105",
                            518: "110/75",
                            519: "130/55",
                            520: "110/65",
                            521: "200/115",
                            522: "180/100",
                            523: "120/75",
                            524: "120/65",
                            525: "150/105",
                            526: "220/85",
                            527: "120/85",
                            528: "180/80",
                            529: "160/70",
                            530: "50/40",
                            531: "130/80",
                            532: "130/95",
                            533: "220/110",
                            534: "190/95",
                            535: "200/85",
                            536: "90/70",
                            537: "160/90",
                            538: "220/120",
                            539: "130/70",
                            540: "190/115",
                            541: "n.m.",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Sättigungsmessgerät anbringen",
            uuid=ActionIDs.SAETTIGUNGSMESSGERAET_ANBRINGEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="passageren Pacer anbringen",
            uuid=ActionIDs.PASSAGEREN_PACER_ANBRINGEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.IV_ZUGANG),
                            str(ActionIDs.ANALGETIKUM),
                        ],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.PASSAGERER_PACER)],
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Perfusorpumpe aktivieren",
            uuid=ActionIDs.PERFUSORPUMPE_AKTIVIEREN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.IV_ZUGANG), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.PERFUSORPUMPE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Perfusorpumpe mit Wirkstoff bestücken",
            uuid=ActionIDs.PERFUSORPUMPE_MIT_WIRKSTOFF_BESTUECKEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.PERFUSORPUMPE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Glucose verabreichen",
            uuid=ActionIDs.GLUCOSE_VERABREICHEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.IV_ZUGANG), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Lyse verabreichen",
            uuid=ActionIDs.LYSE_VERARBREICHEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.IV_ZUGANG), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Patient in benachbarte Station verschieben",
            uuid=ActionIDs.PATIENT_IN_BENACHBARTE_STATION_VERSCHIEBEN,
            defaults={
                "category": "OT",
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,  # Dunno, nothing given
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 2,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 2},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Gerät in andere Station verschieben",
            uuid=ActionIDs.GERAET_IN_ANDERE_STATION_VERSCHIEBEN,
            defaults={
                "category": "OT",
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,  # Dunno, nothing given
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
                            {role_map[RoleIDs.HILFSKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutgaseanalyse für Oxygenierungsleistung durchführen",
            uuid=ActionIDs.BLUTGASEANALYSE_FUER_OXYGENIERUNGSLEISTUNG,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.ART_KANUELE)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BLUTGASANALYSE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "BGA-Oxy": {
                            600: "schwere Hypoxie",
                            601: "leichte Hypoxie",
                            602: "gute Oxygenierung",
                            603: "schwere Hypoxie",
                            604: "mäßige Hypoxie",
                            605: "leichte Hypoxie",
                            606: "mäßige Hypoxie",
                            607: "gute Oxygenierung",
                            608: "leichte Hypoxie",
                            609: "leichte Hypoxie",
                            610: "gute Oxygenierung",
                            611: "schwere Hypoxie",
                            612: "gute Oxygenierung",
                            613: "nicht verwertbar",
                            614: "mäßige Hypoxie",
                            615: "schwere Hypoxie",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutgaseanalyse für Säure-Base-Haushalt durchführen",
            uuid=ActionIDs.BLUTGASEANALYSE_FUER_SAEURE_BASE_HAUSHALT,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            [str(ActionIDs.ART_KANUELE), str(ActionIDs.ZVK)]
                        ],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BLUTGASANALYSE)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "BGA-SBH": {
                            650: "resp. Alkalose",
                            651: "kompensierte resp. Alkalose",
                            652: "kompensierte metabol. Alkalose",
                            653: "metabol. Alkalose",
                            654: "resp. Alkalose",
                            655: "kompensierte resp. Alkalose",
                            656: "ausgeglichener SBH",
                            657: "kompensierte resp. Azidose",
                            658: "kompensierte metab. Azidose",
                            659: "resp. Azidose",
                            660: "kompensierte resp. Azidose",
                            661: "metabol. Azidose",
                            662: "kompensierte resp. Azidose",
                            663: "resp. Azidose",
                            664: "kompensierte resp. Azidose",
                            665: "ausgeglichener SBH",
                            666: "kompensierte resp. Alkalose",
                            667: "metabol. Azidose",
                            668: "resp. Azidose",
                            669: "kompensierte metab. Azidose",
                            670: "ausgeglichener SBH",
                            671: "resp. Azidose",
                            672: "kompensierte metab. Azidose",
                            673: "metabol. Azidose",
                            674: "resp. Alkalose",
                            675: "kompensierte metabol. Alkalose",
                            676: "ausgeglichener SBH",
                            677: "kompensierte resp. Alkalose",
                            678: "metabol. Alkalose",
                            679: "resp. Alkalose",
                            680: "kompensierte metabol. Alkalose",
                            681: "metabol. Alkalose",
                            682: "kompensierte metabol. Alkalose",
                            683: "metabol. Alkalose",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutzucker analysieren",
            uuid=ActionIDs.BLUTZUCKER_ANALYSIEREN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.BZ_MESSGERAET)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "BZ": {
                            900: 265,
                            901: 275,
                            902: 170,
                            903: 285,
                            904: 160,
                            905: 395,
                            906: 125,
                            907: "low",
                            908: 155,
                            909: 165,
                            910: 190,
                            911: 355,
                            912: 130,
                            913: 60,
                            914: 180,
                            915: 50,
                            916: 95,
                            917: 245,
                            918: 30,
                            919: 140,
                            920: 120,
                            921: 335,
                            922: 150,
                            923: 175,
                            924: 55,
                            925: 315,
                            926: 135,
                            927: 85,
                            928: 110,
                            929: 70,
                            930: 80,
                            931: 375,
                            932: 195,
                            933: 45,
                            934: 100,
                            935: 35,
                            936: 75,
                            937: 185,
                            938: 365,
                            939: 205,
                            940: "high",
                            941: 225,
                            942: 90,
                            943: 255,
                            944: 215,
                            945: 20,
                            946: 325,
                            947: 15,
                            948: 385,
                            949: 305,
                            950: 65,
                            951: 40,
                            952: 235,
                            953: 105,
                            954: 115,
                            955: 145,
                            956: 25,
                            957: 295,
                            958: 345,
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="EKG anbringen",
            uuid=ActionIDs.EKG_ANBRINGEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.EKG)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="EKG ablesen",
            uuid=ActionIDs.EKG_ABLESEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.EKG)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "EKG": {
                            701: "Absolute Arrhythmie,Linksschenkelblock",
                            702: "Sinusrhythmus,ST-Streckensenkungen",
                            703: "Schrittmacherrythmus",
                            707: "AV-Block III",
                            709: "Sinusrhythmus,Rechtsschenkelblock",
                            714: "breite Kammerkomplexe",
                            716: "Asystolie",
                            719: "Kammerflimmern",
                            721: "ST-Streckenhebungen, Hinterwandinfarkt",
                            722: "Sinusrhythmus",
                            725: "Sinusrhythmus,vereinzelt Salven",
                            726: "Absolute Arrhythmie,ST-Streckensenkungen",
                            728: "Absolute Arrhythmie,Rechtsschenkelblock",
                            730: "Absolute Arrhythmie,vereinzelt Salven",
                            735: "ST-Streckenhebungen, Hinterwandinfarkt",
                            737: "Sinusrhythmus,vereinzelt sVES",
                            739: "Absolute Arrhythmie,vereinzelt VES",
                            746: "Sinusrhythmus,Linksschenkelblock",
                            747: "Absolute Arrhythmie",
                            748: "Sinusrhythmus,vereinzelt VES",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Zentralen Venendruck messen",
            uuid=ActionIDs.ZENTRALEN_VENENDRUCK_MESSEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.ZVK)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.ZVD_MESSGERAET)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "ZVD": {
                            800: 16,
                            801: 12,
                            802: -5,
                            803: 14,
                            804: 6,
                            805: 1,
                            806: -14,
                            807: 13,
                            808: 17,
                            809: 19,
                            810: 3,
                            811: -12,
                            812: 9,
                            813: 5,
                            814: -3,
                            815: -10,
                            816: -15,
                            817: -9,
                            818: 22,
                            819: 21,
                            820: 11,
                            821: 4,
                            822: 0,
                            823: -2,
                            824: 10,
                            825: -13,
                            826: 23,
                            827: -6,
                            828: -7,
                            829: -8,
                            830: 20,
                            831: -4,
                            832: 15,
                            833: 8,
                            834: 18,
                            835: -11,
                            836: 7,
                            837: 2,
                            838: -1,
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Extremitäten Röntgen",
            uuid=ActionIDs.EXTREMITAETEN_ROENTGEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 240,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.ROENTGENGERAET)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.MTRA]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Rö-Extremitäten": {
                            511: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            512: "Dislozierte Handgelenksfraktur; sonst keine Frakturen",
                            520: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            523: "HüftTEP; sonst keine Auffälligkeiten",
                            524: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            525: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            527: "Extremitäten: Oberschenkelfraktur bds. im mittleren Drittel;",
                            530: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            558: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            559: "Spiralfraktur rechter Oberarm; sonst keine Frakturen",
                            563: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            564: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            566: "Oberschenkelfraktur re;",
                            567: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            571: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            573: "komplette Unterarmfraktur li. mit dezenter Verschiebung;",
                            579: "Extremitäten: Normalbefund; keine Frakturzeichen; mehrere Fremdkörper in beiden Händen;",
                            584: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            586: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            590: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            591: "fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.;",
                            600: "nicht dislozierte Sprunggelengsfraktur; sonst Extr. OB.",
                            602: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            607: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            608: "Sprunggelenksfraktur mit deutlicher Dislokation",
                            609: "fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.;",
                            617: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            619: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            625: "Trümmerfraktur des distalen US re.; komplette proximale Unterarmfraktur re.",
                            637: "Oberschenkeltrummerfraktur re.",
                            640: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            649: "Oberschenkelschaftfraktur li mit Fehlstellung",
                            650: "Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper;",
                            652: "fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.;",
                            664: "Oberarmamputation li.; sonst keine Frakturzeichen oder Fremdkörper;",
                            675: "fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.;",
                            680: "komplette Unterarmfraktur re.",
                            681: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                            682: "Extremitäten: Normalbefund; keine Frakturzeichen;",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Thorax Röntgen",
            uuid=ActionIDs.THORAX_ROENTGEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 240,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.ROENTGENGERAET)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.MTRA]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Rö-Thorax": {
                            305: "Lunge noch deutlich überwässert; Pleuraergüsse bds.",
                            306: "Thorax: Normalbefund;",
                            307: "Thorax: Normalbefund;",
                            312: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand",
                            314: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung",
                            324: "Rippenserienfraktur re. 4-7; Lunge seitengleich ventiliert",
                            327: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung; Metallcerclage wie nach Sternotomie;",
                            334: "deutlich vergrößertes Herz, Aorta elongiert, Belüftung oB.",
                            336: "Thorax: Normalbefund;",
                            339: "Thorax: Normalbefund;",
                            340: "Pneumothorax re. ca. 2 cm",
                            341: "Thorax: Normalbefund;",
                            342: "Rippenserienfraktur re. 3-7 ohne Pneu",
                            343: "sgl Belüftung; beginnende Infiltrate bds. Basal",
                            347: "Thorax: deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; keine Frakturen, gleiche Belüftung",
                            361: "Thorax: großes Herz, geringgradige Stauung der Lunge, Belüftung seitengleich",
                            370: "Thorax: Normalbefund;",
                            375: "sgl Belüftung; beginnende Infiltrate bds. Basal, kleine Ergüsse",
                            376: "inhomogene Verschattungen, bds zentrale Infiltrate",
                            377: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen",
                            381: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 3 cm; wenig Blut im unteren Resessus re.; beginnendes Hautemphysem re. lateral; Lunge seitengleich ventiliert",
                            382: "Thorax: Lobärpneumonie links; deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; seitengleiche Belüftung",
                            388: "Thorax: Normalbefund;",
                            389: "Thorax: Normalbefund;",
                            401: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 1,5 cm; wenig Blut im unteren Resessus re.; Lunge seitengleich ventiliert",
                            414: "leichte Stauungszeichen hilär",
                            418: "Thorax: Normalbefund;",
                            422: "Thorax: Normalbefund;",
                            427: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand",
                            428: "Thorax: Normalbefund;",
                            429: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen",
                            432: "Thorax: Normalbefund;",
                            435: "Sternumfraktur im mittleren Drittel",
                            445: "Thorax: seitengleiche Belüftung; keine Ergüsse; kein Pneu; Rippenserienfraktur rechts lateral 3-6;",
                            446: "Pleuraergüsse bds, Lunge inhomogen verschattet, Belüftung seitengleich, Thoraxskelet oB;",
                            457: "linke Lunge deutlich überbläht, Mediastinum dezent nach links verschoben; mehrere große Bullae; basal bds Infiltrate, Herz grenzwertig groß wie bei Rechtsbelastung",
                            460: "inhomogene Verschattungen, bds zentrale Infiltrate. Zwerchfellhochstand",
                            471: "seitengleiche Belüftung; keine Ergüsse; kein Pneu; nicht dislozierte, sternumnahe Fraktur 4.Rippe li.;",
                            479: "Schrittmacheraggregat links subclavikulär, Kabel an loco tipico, Lunge dezent parahilär gestaut, keine Ergüsse;",
                            485: "Rippenserienfraktur re. 4-7; kompletter Pneumothorax re. mit Verlagerung des gesamten Mediastinums; ausgedehntes Hautemphysem; Lunge nur links ventiliert",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Trauma CT",
            uuid=ActionIDs.TRAUMA_CT,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": True,
                "application_duration": 300,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 3,
                        "lab_devices": [str(MaterialIDs.COMPUTERTOMOGRAPHIE)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.MTRA]: 1},
                            {role_map[RoleIDs.ARZT]: 1},
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Trauma-CT": {
                            100: "deutlich vergrößertes Herz, Aorta elongiert, Belüftung oB. Extremitäten: Normalbefund; keine Frakturzeichen;",
                            105: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales vermutlich gekapseltes Hämatom abdominal ca 2 L",
                            106: "Thorax: Normalbefund; Spiralfraktur rechter Oberarm; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            108: "leichte Stauungszeichen hilär komplette Unterarmfraktur re.",
                            112: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 3 cm; wenig Blut im unteren Resessus re.; beginnendes Hautemphysem re. lateral; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            121: "Thorax: Normalbefund; komplette Unterarmfraktur li. mit dezenter Verschiebung. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            123: "inhomogene Verschattungen, bds zentrale Infiltrate. Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales gekapseltes Hämatom abdominal mind 2 L",
                            130: "seitengleiche Belüftung; keine Ergüsse; kein Pneu; nicht dislozierte, sternumnahe Fraktur 4.Rippe li.; Oberarmamputation li.; sonst keine Frakturzeichen oder Fremdkörper; HWS: oB.; Becken: oB.;",
                            135: "Rippenserienfraktur re. 4-7; Mantelpneu re. ca 1,5 cm; wenig Blut im unteren Resessus re.; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            136: "inhomogene Verschattungen, bds zentrale Infiltrate Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; kleines zentrales Hämatom abdominal ca. 300 ml",
                            137: "Rippenserienfraktur re. 4-7; kompletter Pneumothorax re. mit Verlagerung des gesamten Mediastinums; ausgedehntes Hautemphysem; Lunge nur links ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            148: "Lunge noch deutlich überwässert; Pleuraergüsse bds. Extremitäten: Normalbefund; keine Frakturzeichen;",
                            152: "sgl Belüftung; beginnende Infiltrate bds. Basal, kleine Ergüsse Extremitäten: Normalbefund; keine Frakturzeichen; mind. 1 L Aszites; Pankreas aufgelockert, mehrere Pseudozysten",
                            159: "Thorax: Normalbefund; Oberschenkelfraktur re; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            161: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung; Metallcerclage wie nach Sternotomie;",
                            162: "Thorax: deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; keine Frakturen, gleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            173: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 2 l Blut im Abdomen; Leber fraglich rupturiert.",
                            174: "Thorax: großes Herz, geringgradige Stauung der Lunge, Belüftung seitengleich HüftTEP; sonst keine Auffälligkeiten",
                            175: "sgl Belüftung; beginnende Infiltrate bds. Basal Extremitäten: Normalbefund; keine Frakturzeichen;",
                            176: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; dezente Mittelllinienverschiebung; beginnendes Hirnödem linkshemisphärisch;",
                            185: "inhomogene Verschattungen, bds zentrale Infiltrate, Zwerchfellhochstand Extremitäten: Normalbefund; keine Frakturzeichen; Lunge wie bei ARDS; zentrales ausgedehntes Hämatom abdominal mind 2 - 2,5 L",
                            189: "Rippenserienfraktur re. 4-7; Lunge seitengleich ventiliert fragliche Fissur rechter Oberarmkopf; sonstige Extremitäten oB.; HWS: oB:; Becken: oB:; Schädel: oB.;",
                            191: "Thorax: Zwerchfellhochstand bds.; Belüftung sgl.; keine Frakturzeichen Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 3 l Blut im Abdomen; Leber fraglich rupturiert.",
                            196: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; Dünndarmschlingen aufgetrieben, Darmwand im Ileumbereich deutlich verdickt, ca. 200 ml freie Flüssigkeit",
                            205: "Thorax: Normalbefund; Dislozierte Handgelenksfraktur; sonst keine Frakturen HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            207: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1 l Blut im Abdomen; Leber fraglich rupturiert.",
                            209: "minimale pulmonale Stauungszeichen im Hilusbereich, seitengleiche Belüftung Oberschenkeltrummerfraktur re.",
                            221: "Sternumfraktur im mittleren Drittel Sprunggelenksfraktur mit deutlicher Dislokation",
                            228: "Thorax: Normalbefund; nicht dislozierte Sprunggelengsfraktur; sonst Extr. OB. HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: Nasenbeinfraktu; fragliche Orbitabodenfraktur re.; fragliche Fissur Occipital; keine ICB, keine Raumforderung;",
                            236: "linke Lunge deutlich überbläht, Mediastinum dezent nach links verschoben; mehrere große Bullae; basal bds Infiltrate, Herz grenzwertig groß wie bei Rechtsbelastung Extremitäten: Normalbefund; keine Frakturzeichen;",
                            237: "Thorax: seitengleiche Belüftung; keine Ergüsse; kein Pneu; Rippenserienfraktur rechts lateral 3-6; Extremitäten: Oberschenkelfraktur bds. im mittleren Drittel;",
                            238: "Pleuraergüsse bds, Lunge inhomogen verschattet, Belüftung seitengleich, Thoraxskelet oB; Extremitäten: Normalbefund; keine Frakturzeichen;",
                            242: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            243: "Schrittmacheraggregat links subclavikulär, Kabel an loco tipico, Lunge dezent parahilär gestaut, keine Ergüsse; Extremitäten: Normalbefund; keine Frakturzeichen;",
                            248: "Rippenserienfraktur re. 3-7 ohne Pneu Trümmerfraktur des distalen US re.; komplette proximale Unterarmfraktur re.",
                            260: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; mehrere Fremdkörper in beiden Händen; HWS: oB.; Becken: oB; Abdomen: oB.; Schädel: oB.;",
                            269: "Pneumothorax re. ca. 2 cm Oberschenkelschaftfraktur li mit Fehlstellung",
                            273: "Thorax: Lobärpneumonie links; deutliche Überblähung der peripheren Lungenanteile, vereinzelt kleinere Bullä; seitengleiche Belüftung Extremitäten: Normalbefund; keine Frakturzeichen; Pneumonische Infiltrate links und beginnend rechts, kleiner Pleuraerguss re.",
                            274: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; mind 1,5 l Blut im Abdomen; Leber fraglich rupturiert.",
                            281: "Thorax: Normalbefund; Extremitäten: Normalbefund; keine Frakturzeichen; keine Fremdkörper; HWS: oB.; Becken: oB.; Schädel: knöchern oB.; ca 1 cm großes Subduralhämatom li frontal; keine Mittelllinienverschiebung; kein Hirnödem;",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Ultraschall Abdomen",
            uuid=ActionIDs.ULTRASCHALL_ABDOMEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.SONOGRAPHIE)],
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
                        "Ultraschall": {
                            502: "schlechte Untersuchungsbedingungen; mind 2-3 L freie Flüssigkeit im gesamten Abdomen",
                            509: "Leber inhomogen, keine Aszites",
                            513: "wenig freie Flüssigkeit im kleinen Becken",
                            519: "freie Flüssigkeit im kleinen Becken (ca 100 ml)",
                            522: "fraglich kleines Hämatom im mittleren Abdomenbereich",
                            541: "schlechte Untersuchungsbedingungen; Darmwand im Ileumbereich deutlich verdickt, ca. 500 ml freie Flüssigkeit im Douglas und um die Leber",
                            559: "deutlich freie Flüssigkeit im kleinen Becken (> 500 ml) und um die Leber",
                            565: "massiv freie Flüssigkeit im gesamten Abdomen (> 2000 ml)",
                            566: "Schlechte Untersuchungsbedingugen. Freie Flüssigkeit auszuschließen.",
                            571: "reichlich Aszites; Leber oB.; Pankreas aufgelockert, mehrere Pseudozysten",
                            585: "Abdomen o.B.; V.a. Pneumothorax re.",
                            589: "keine Pleuraergüsse; keine freie Flüssigkeit im Abdomen; Bauch- und Beckenorgane o.B.",
                            591: "großes Hämatom im mittleren Abdomenbereich, viel gekapselte Flüssigkeit um die Aorta",
                            612: "großes Hämatom im mittleren Abdomenbereich, viel gekapselte Flüssigkeit um die Aorta",
                            614: "freie Flüssigkeit im kleinen Becken und um die Milz",
                            615: "Abdomen; Normalbefund; keine pathologischen Veränderungen; Thorax: keine Ergüsse sichtbar",
                            621: "Abdomen o.B.; Schwangerschaft mit vitalem Kind",
                            624: "schlechte Untersuchungsbedingungen; viel freie Flüssigkeit im Becken und um die Leber",
                            626: "schlechte Untersuchungsbedingungen; massive freie Flüssigkeit im gesamten Abdomen",
                            647: "Abdomen; Normalbefund; keine pathologischen Veränderungen;",
                            658: "sehr großes Hämatom im mittleren Abdomenbereich, massiv Flüssigkeit um die Aorta",
                            665: "schlechte Untersuchungsbedingungen; mind 1,5 L freie Flüssigkeit im Becken und um die Leber",
                            686: "deutlich verkleinerte Leber mit erhöhter Dichte, mind 1,5 L Aszites",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Ultraschall Thorax",
            uuid=ActionIDs.ULTRASCHALL_THORAX,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 60,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.SONOGRAPHIE)],
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
                        "Ultraschall": {
                            502: "schlechte Untersuchungsbedingungen; mind 2-3 L freie Flüssigkeit im gesamten Abdomen",
                            509: "Leber inhomogen, keine Aszites",
                            513: "wenig freie Flüssigkeit im kleinen Becken",
                            519: "freie Flüssigkeit im kleinen Becken (ca 100 ml)",
                            522: "fraglich kleines Hämatom im mittleren Abdomenbereich",
                            541: "schlechte Untersuchungsbedingungen; Darmwand im Ileumbereich deutlich verdickt, ca. 500 ml freie Flüssigkeit im Douglas und um die Leber",
                            559: "deutlich freie Flüssigkeit im kleinen Becken (> 500 ml) und um die Leber",
                            565: "massiv freie Flüssigkeit im gesamten Abdomen (> 2000 ml)",
                            566: "Schlechte Untersuchungsbedingugen. Freie Flüssigkeit auszuschließen.",
                            571: "reichlich Aszites; Leber oB.; Pankreas aufgelockert, mehrere Pseudozysten",
                            585: "Abdomen o.B.; V.a. Pneumothorax re.",
                            589: "keine Pleuraergüsse; keine freie Flüssigkeit im Abdomen; Bauch- und Beckenorgane o.B.",
                            591: "großes Hämatom im mittleren Abdomenbereich, viel gekapselte Flüssigkeit um die Aorta",
                            612: "großes Hämatom im mittleren Abdomenbereich, viel gekapselte Flüssigkeit um die Aorta",
                            614: "freie Flüssigkeit im kleinen Becken und um die Milz",
                            615: "Abdomen; Normalbefund; keine pathologischen Veränderungen; Thorax: keine Ergüsse sichtbar",
                            621: "Abdomen o.B.; Schwangerschaft mit vitalem Kind",
                            624: "schlechte Untersuchungsbedingungen; viel freie Flüssigkeit im Becken und um die Leber",
                            626: "schlechte Untersuchungsbedingungen; massive freie Flüssigkeit im gesamten Abdomen",
                            647: "Abdomen; Normalbefund; keine pathologischen Veränderungen;",
                            658: "sehr großes Hämatom im mittleren Abdomenbereich, massiv Flüssigkeit um die Aorta",
                            665: "schlechte Untersuchungsbedingungen; mind 1,5 L freie Flüssigkeit im Becken und um die Leber",
                            686: "deutlich verkleinerte Leber mit erhöhter Dichte, mind 1,5 L Aszites",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Kreuzblut",
            uuid=ActionIDs.KREUZBLUT,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTGRUPPE_BESTIMMEN),
                            str(ActionIDs.BLUTABNAHME),
                        ],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.BLUTBANK)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Kreuzblut": {
                            1000: "Erfolg! Das getestete Blut ist kompatibel.",
                            1001: "Misserfolg! Das getestete Blut ist inkompatibel.",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Blutgruppe bestimmen",
            uuid=ActionIDs.BLUTGRUPPE_BESTIMMEN,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 180,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.BLUTABNAHME)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.BLUTBANK)],
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
        Action.objects.update_or_create(
            name="Hämoglobinanalyse",
            uuid=ActionIDs.HAEMOGLOBINANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [
                            [
                                str(MaterialIDs.LAB_GERAET_1),
                                str(MaterialIDs.BLUTGASANALYSE),
                            ]
                        ],
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
            name="Lactatanalyse",  # can also be written as "Laktatanalyse"
            uuid=ActionIDs.LACTATANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.LAB_GERAET_1)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Lactat": {
                            140: "negativ",
                            141: "stark positiv",
                            142: "negativ",
                            143: "stark positiv",
                            144: "grenzwertig positiv",
                            145: "grenzwertig positiv",
                            146: "negativ",
                            147: "grenzwertig positiv",
                            148: "stark positiv",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Gerinnungsanalyse",
            uuid=ActionIDs.GERINNUNGSANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.LAB_GERAET_2)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Gerinnung": {
                            100: "leichte Einschränkung",
                            101: "Normalwerte",
                            102: "leichte Einschränkung",
                            103: "leichte Einschränkung",
                            104: "Normalwerte",
                            105: "Normalwerte",
                            106: "schwere Einschränkung",
                            107: "schwere Einschränkung",
                            108: "schwere Einschränkung",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Leberanalyse",
            uuid=ActionIDs.LEBERANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.LAB_GERAET_3)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Leber": {
                            110: "Normalwerte",
                            111: "leichte Einschränkung",
                            112: "schwere Einschränkung",
                            113: "schwere Einschränkung",
                            114: "leichte Einschränkung",
                            115: "Normalwerte",
                            116: "leichte Einschränkung",
                            117: "Normalwerte",
                            118: "schwere Einschränkung",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Nierenanalyse",
            uuid=ActionIDs.NIERENANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.LAB_GERAET_3)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Niere": {
                            120: "schwere Einschränkung",
                            121: "schwere Einschränkung",
                            122: "Normalwerte",
                            123: "leichte Einschränkung",
                            124: "leichte Einschränkung",
                            125: "leichte Einschränkung",
                            126: "Normalwerte",
                            127: "Normalwerte",
                            128: "schwere Einschränkung",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Infarktanalyse",
            uuid=ActionIDs.INFARKTANALYSE,
            defaults={
                "category": Action.Category.EXAMINATION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 120,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.BLUTABNAHME)
                        ],  # This is WIP, as you actually need to have done a blood draw per action
                        # with blood draw as requirement, which also need to be unique per patient
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [str(MaterialIDs.LAB_GERAET_3)],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "Infarkt": {
                            130: "stark positiv",
                            131: "negativ",
                            132: "stark positiv",
                            133: "negativ",
                            134: "grenzwertig positiv",
                            135: "negativ",
                            136: "stark positiv",
                            137: "grenzwertig positiv",
                            138: "grenzwertig positiv",
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Lyophilisiertes Frischplasma auflösen",
            uuid=ActionIDs.LYOPHILISIERTES_FRISCHPLASMA_VORBEREITEN,
            defaults={
                "category": Action.Category.PRODUCTION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 300,
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
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {
                        "produced_material": {
                            str(MaterialIDs.LYOPHILISIERTES_FRISCHPLASMA): 1
                        }
                    }
                ),
            },
        )
        Action.objects.update_or_create(
            name="Lyophilisiertes Frischplasma anwenden",
            uuid=ActionIDs.LYOPHILISIERTES_FRISCHPLASMA_ANWENDEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.LYOPHILISIERTES_FRISCHPLASMA)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma auftauen",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_VORBEREITEN,
            defaults={
                "category": Action.Category.PRODUCTION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 420,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [
                            str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)
                        ],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {"produced_material": {str(MaterialIDs.FRESH_FROZEN_PLASMA): 1}}
                ),
            },
        )
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma anwenden",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_ANWENDEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": [str(MaterialIDs.FRESH_FROZEN_PLASMA)],
                        "num_personnel": 1,
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
        Action.objects.update_or_create(
            name="Enthrozytenkonzentrat erwärmen",
            uuid=ActionIDs.ENTHROZYTENKONZENTRATE_VORBEREITEN,
            defaults={
                "category": Action.Category.PRODUCTION,
                "location": Action.Location.LAB,
                "relocates": False,
                "application_duration": 360,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": None,
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,
                        "lab_devices": [
                            str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)
                        ],
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        ],
                    },
                ),
                "results": json.dumps(
                    {"produced_material": {str(MaterialIDs.ENTHROZYTENKONZENTRAT): 1}}
                ),
            },
        )
        Action.objects.update_or_create(
            name="Enthrozytenkonzentrate anwenden",
            uuid=ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.BEDSIDE,
                "relocates": False,
                "application_duration": 15,
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [
                            str(ActionIDs.IV_ZUGANG),
                            str(ActionIDs.KREUZBLUT),
                        ],
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
            },
        )
        Action.objects.update_or_create(
            name="Operation einleiten",
            uuid=ActionIDs.OP_EINLEITEN,
            defaults={
                "category": Action.Category.TREATMENT,
                "location": Action.Location.LAB,
                "relocates": True,
                "application_duration": 360000,  # 100h to assure that the operation never finishes during an exercise
                "effect_duration": None,
                "conditions": json.dumps(
                    {
                        "required_actions": [str(ActionIDs.IV_ZUGANG)],
                        "prohibitive_actions": None,
                        "material": None,
                        "num_personnel": 1,  # garbage values
                        "lab_devices": None,
                        "area": None,
                        "role": [
                            {role_map[RoleIDs.ARZT]: 1},
                        ],
                    },
                ),
            },
        )
