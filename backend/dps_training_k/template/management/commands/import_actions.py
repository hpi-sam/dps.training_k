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
        Action.objects.update_or_create(
            name="Beatmung",
            uuid=ActionIDs.BEATMUNG,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
                    "required_actions": [str(ActionIDs.TRACHEALTUBUS)],
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.BEATMUNGSGERAET)],
                    "num_personnel": 2,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Thoraxdrainage",
            uuid=ActionIDs.THORAXDRAINAGE,
            defaults={
                "category": "TR",
                "application_duration": 300,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Pleurapunktion",
            uuid=ActionIDs.PLEURAPUNKTION,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Trachealtubus",
            uuid=ActionIDs.TRACHEALTUBUS,
            defaults={
                "category": "TR",
                "application_duration": 120,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Larynxmaske",
            uuid=ActionIDs.LARYNXMASKE,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Larynxtubus",
            uuid=ActionIDs.LARYNXTUBUS,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Guedeltubus",
            uuid=ActionIDs.GUEDELTUBUS,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Wendeltubus",
            uuid=ActionIDs.WENDELTUBUS,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Koniotomietubus",
            uuid=ActionIDs.KONIOTOMIETUBUS,
            defaults={
                "category": "TR",
                "application_duration": 180,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Analgetikum",
            uuid=ActionIDs.ANALGETIKUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 600,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Antiasthmatikum",
            uuid=ActionIDs.ANTIASTHMATIKUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 600,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Kortikosteroid",
            uuid=ActionIDs.KORTIKOSTEROID,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 1800,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Nitrat",
            uuid=ActionIDs.NITRAT,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 600,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Diuretikum",
            uuid=ActionIDs.DIURETIKUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 1200,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Katecholamin",
            uuid=ActionIDs.KATECHOLAMIN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 60,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Sedativum",
            uuid=ActionIDs.SEDATIVUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 600,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Regional-Narkotikum",
            uuid=ActionIDs.REGIONAL_NARKOTIKUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # "Freifeld", dunno how do handle that
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Tetanusprophylaxe",
            uuid=ActionIDs.TETANUSPROPHYLAXE,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Antikoagulanz",
            uuid=ActionIDs.ANTIKOAGULANZ,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="(Voll-)Narkotikum",
            uuid=ActionIDs.NARKOTIKUM,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,  # None means permanent
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Vollelektrolyt",
            uuid=ActionIDs.VOLLELEKTROLYT,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120,  # Depends of type of "Zugang"
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Plasmaexpander",
            uuid=ActionIDs.PLASMAEXPANDER,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120,  # Depends of type of "Zugang"
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="i.V. Zugang",
            uuid=ActionIDs.IV_ZUGANG,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": 120,  # depends on type of "Zugang"
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="ZVK",
            uuid=ActionIDs.ZVK,
            defaults={
                "category": "TR",
                "application_duration": 300,
                "effect_duration": 360,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Schleuse",
            uuid=ActionIDs.SCHLEUSE,
            defaults={
                "category": "TR",
                "application_duration": 240,
                "effect_duration": 60,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="art. Kanüle",
            uuid=ActionIDs.ART_KANUELE,
            defaults={
                "category": "TR",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="mehrlumen ZVK",
            uuid=ActionIDs.MEHRLUMEN_ZVK,
            defaults={
                "category": "TR",
                "application_duration": 240,
                "effect_duration": 420,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Regional-Narkose",
            uuid=ActionIDs.REGIONAL_NARKOSE,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": None,  # abhängig von Medikament
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="ZVD",
            uuid=ActionIDs.ZVD,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Druckverband",
            uuid=ActionIDs.DRUCKVERBAND,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Turniquet",
            uuid=ActionIDs.TURNIQUET,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Wundversorgung",
            uuid=ActionIDs.WUNDVERSORGUNG,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="chir. Blutstillung",
            uuid=ActionIDs.CHIR_BLUTSTILLUNG,
            defaults={
                "category": "TR",
                "application_duration": 180,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Stifneck",
            uuid=ActionIDs.STIFNECK,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Vakuumschiene",
            uuid=ActionIDs.VAKUUMSCHIENE,
            defaults={
                "category": "TR",
                "application_duration": 60,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Beckenschlinge",
            uuid=ActionIDs.BECKENSCHLINGE,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Gipsverband",
            uuid=ActionIDs.GIPSVERBAND,
            defaults={
                "category": "TR",
                "application_duration": 300,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Stabile Seitenlage",
            uuid=ActionIDs.STABILE_SEITENLAGE,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Schocklage",
            uuid=ActionIDs.SCHOCKLAGE,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Defi + transcutaner Pacer",
            uuid=ActionIDs.DEFI_TRANSCUTANER_PACER,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [
                        str(ActionIDs.IV_ZUGANG),
                        [str(ActionIDs.NARKOTIKUM), str(ActionIDs.ANALGETIKUM)],
                    ],
                    "prohibitive_actions": None,
                    "material": str(MaterialIDs.DEFIBRILATOR),
                    "num_personnel": 2,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Beatmungsgerät anbringen",
            uuid=ActionIDs.BEATMUNGSGERAET_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [
                        str(ActionIDs.IV_ZUGANG),
                        str(ActionIDs.NARKOTIKUM),
                        [
                            str(ActionIDs.TRACHEALTUBUS),
                            str(ActionIDs.LARYNXTUBUS),
                            str(ActionIDs.LARYNXMASKE),
                        ],
                    ],
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.BEATMUNGSGERAET)],
                    "num_personnel": 2,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Sauerstoff anbringen",
            uuid=ActionIDs.SAUERSTOFF_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Blutdruckmessgerät anbringen",
            uuid=ActionIDs.BLUTDRUCK_MESSGERAET_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Sättigungsmessgerät anbringen",
            uuid=ActionIDs.SAETTIGUNGSMESSGERAET_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Monitor anbringen",
            uuid=ActionIDs.MONITOR_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="passageren Pacer anbringen",
            uuid=ActionIDs.PASSAGEREN_PACER_ANBRINGEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [
                        str(ActionIDs.IV_ZUGANG),
                        str(ActionIDs.ANALGETIKUM),
                    ],
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.DEFIBRILATOR)],
                    "num_personnel": 2,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Perfusorpumpe aktivieren",
            uuid=ActionIDs.PERFUSORPUMPE_AKTIVIEREN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Perfusorpumpe mit Wirkstoff bestücken",
            uuid=ActionIDs.PERFUSORPUMPE_MIT_WIRKSTOFF_BESTUECKEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Glucose verabreichen",
            uuid=ActionIDs.GLUCOSE_VERABREICHEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Lyse verabreichen",
            uuid=ActionIDs.LYSE_VERARBREICHEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Patient in benachbarte Station verschieben",
            uuid=ActionIDs.PATIENT_IN_BENACHBARTE_STATION_VERSCHIEBEN,
            defaults={
                "category": "OT",
                "application_duration": 0,  # Dunno, nothing given
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Gerät in andere Station verschieben",
            uuid=ActionIDs.GERAET_IN_ANDERE_STATION_VERSCHIEBEN,
            defaults={
                "category": "OT",
                "application_duration": 0,  # Dunno, nothing given
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma (jegliche Blutgruppe) auftauen",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_AUFTAUEN,
            defaults={
                "category": "OT",
                "application_duration": 420,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Lyophilisiertes Frischplasma (jegliche Blutgruppe) auftauen",
            uuid=ActionIDs.LYOPHILISIERTES_FRISCHPLASMA_AUFTAUEN,
            defaults={
                "category": "OT",
                "application_duration": 420,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.WAERMEGERAET_FUER_BLUTPRODUKTE)],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Blutgaseanalyse für Oxygenierungsleistung durchführen",
            uuid=ActionIDs.BLUTGASEANALYSE_FUER_OXYGENIERUNGSLEISTUNG,
            defaults={
                "category": "EX",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [str(ActionIDs.ART_KANUELE)],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Blutgaseanalyse für Säure-Base-Haushalt durchführen",
            uuid=ActionIDs.BLUTGASEANALYSE_FUER_SAEURE_BASE_HAUSHALT,
            defaults={
                "category": "EX",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [
                        [str(ActionIDs.ART_KANUELE), str(ActionIDs.ZVK)]
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
            },
        )
        Action.objects.update_or_create(
            name="Blutzucker analysieren",
            uuid=ActionIDs.BLUTZUCKER_ANALYSIEREN,
            defaults={
                "category": "EX",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="EKG anbringen",
            uuid=ActionIDs.EKG_ANBRINGEN,
            defaults={
                "category": "EX",
                "application_duration": 60,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Zentralen Venendruck messen",
            uuid=ActionIDs.ZENTRALEN_VENENDRUCK_MESSEN,
            defaults={
                "category": "EX",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Extremitäten Röntgen",
            uuid=ActionIDs.EXTREMITAETEN_ROENTGEN,
            defaults={
                "category": "EX",
                "application_duration": 240,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.MTRA]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Thorax Röntgen",
            uuid=ActionIDs.THORAX_ROENTGEN,
            defaults={
                "category": "EX",
                "application_duration": 240,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.MTRA]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Traume CT",
            uuid=ActionIDs.TRAUME_CT,
            defaults={
                "category": "EX",
                "application_duration": 300,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 3,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.MTRA]: 1},
                        {role_map[RoleIDs.ARZT]: 1},
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Ultraschall Abdomen",
            uuid=ActionIDs.ULTRASCHALL_ABDOMEN,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Ultraschall Thorax",
            uuid=ActionIDs.ULTRASCHALL_THORAX,
            defaults={
                "category": "EX",
                "application_duration": 60,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Kreuzblut",
            uuid=ActionIDs.KREUZBLUT,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Blutgruppe bestimmen",
            uuid=ActionIDs.BLUTGRUPPE_BESTIMMEN,
            defaults={
                "category": "EX",
                "application_duration": 180,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Hämoglobinanalyse",
            uuid=ActionIDs.HAEMOGLOBINANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Lactatanalyse",
            uuid=ActionIDs.LACTATANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [str(MaterialIDs.BGA_GERAET)],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Gerinnungsanalyse",
            uuid=ActionIDs.GERINNUNGSANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None, # "Laboranalyse"???
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Leberanalyse",
            uuid=ActionIDs.LEBERANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Nierenanalyse",
            uuid=ActionIDs.NIERENANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Infarktanalyse",
            uuid=ActionIDs.INFARKTANALYSE,
            defaults={
                "category": "EX",
                "application_duration": 120,
                "effect_duration": None,
                "conditions": {
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
            },
        )
        Action.objects.update_or_create(
            name="Fresh Frozen Plasma anwenden",
            uuid=ActionIDs.FRESH_FROZEN_PLASMA_ANWENDEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120, # depends on type of "Zugang"
                "conditions": {
                    "required_actions": [str(ActionIDs.IV_ZUGANG)],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Enthrozytenkonzentrate anwenden",
            uuid=ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": 120, # depends on type of "Zugang"
                "conditions": {
                    "required_actions": [str(ActionIDs.IV_ZUGANG)],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
        Action.objects.update_or_create(
            name="Enthrozytenkonzentrate (jegliche Blutgruppe) anwenden",
            uuid=ActionIDs.ENTHROZYTENKONZENTRATE_JEGLICHE_BLUTGRUPPE_ANWENDEN,
            defaults={
                "category": "TR",
                "application_duration": 0,
                "effect_duration": None,
                "conditions": {
                    "required_actions": [str(ActionIDs.IV_ZUGANG)],
                    "prohibitive_actions": None,
                    "material": None,
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [
                        {role_map[RoleIDs.ARZT]: 1},
                    ],
                },
            },
        )
