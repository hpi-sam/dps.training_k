from uuid import UUID

from django.core.management import call_command
from django.core.management.base import BaseCommand

from configuration import settings
from game.models import Exercise, PatientInstance, Area, Personnel
from template.constants import ActionIDs
from template.models import Action, Material


class StuffIDs:
    JUENGER = UUID("8c2f0037-9fbe-413a-8921-1a197f2cb464")
    CAPTURE_THE_FLAG = UUID("e7db5350-7fa2-43fc-b89a-57f7554937af")
    MONEY = UUID("84aaad32-8df1-4499-88f7-5704601355fe")
    OLYMPIA_RANGLISTENPUNKTE = UUID("62431fc5-7276-4fac-a972-054d7c45d12a")
    ISSUE = UUID("0108b8dc-4d4d-40bc-89b0-53c3f7cff48e")
    RETRO_PHOTO = UUID("f4ac3d26-bb8c-4e9d-83ef-4462a171dbc3")
    CLAAS_VERSCHLAEFT = UUID("0b8eb900-5003-4e57-a76b-9158c1cc646c")


class ActionIDs:
    GLAUBENSFRAGEN_VOR_DER_MENSA_STELLEN = UUID("3100f1da-b450-48e4-93af-5ee796743d02")
    PCG_PROGRAMMIEREN = UUID("e0fda5bf-4431-447a-91c9-a443381902cd")
    MFC_PROGRAMMIEREN = UUID("5f0418a9-6116-4ae0-9aee-b72eacae3b06")
    TISCHTENNIS_TRAINIEREN = UUID("b61a85f3-95ec-406f-8355-690979ebb443")
    ISSUE_BEARBEITEN = UUID("565e4bad-64d3-43d9-9516-50bd5d6f18ab")
    TTT_UM_10 = UUID("d67005e5-33ed-47ed-b0dd-dd35624b8616")
    TTT_UM_10_30 = UUID("36787763-0676-46fa-a886-e154246ccafb")


class Command(BaseCommand):
    help = "Creates a basic exercise one can join immediately without having to create it via the trainer interface first."

    def handle(self, *args, **options):
        call_command("flush", "--noinput")
        import_patients("./data/patient_information.csv")  # path to the csv file
        self.stdout.write(self.style.SUCCESS("Successfully imported patient data"))

        self.create_a_2_3()
        self.stdout.write(self.style.SUCCESS("Successfully A-2.3 to the database"))
        self.create_stuff()
        self.create_work()
        self.stdout.write(
            self.style.SUCCESS("Successfully added BP-2023 HG to the database")
        )

    @staticmethod
    def create_stuff():
        Material.objects.update_or_create(
            uuid=StuffIDs.JUENGER,
            name="Jünger (m/w/d)",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.CAPTURE_THE_FLAG,
            name="Capture the Flag Aufgabe. Ohne Clicky-Bunty",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.MONEY,
            name="Geld von Fitnessnerds",
            category=Material.Category.DEVICE,
            is_reusable=False,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.OLYMPIA_RANGLISTENPUNKTE,
            name="Olympia Ranglistenpunkte/ Kreisklassenpunkte",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.ISSUE,
            name="Codezeilen, die nicht funktionieren",
            category=Material.Category.DEVICE,
            is_reusable=False,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.RETRO_PHOTO,
            name="Retro Foto",
            category=Material.Category.DEVICE,
            is_reusable=True,
        )
        Material.objects.update_or_create(
            uuid=StuffIDs.CLAAS_VERSCHLAEFT,
            name="Claas verschläft",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )

    @staticmethod
    def create_work():
        Action.objects.update_or_create(
            name="Glaubensfragen vor der Mensa stellen",
            uuid=ActionIDs.GLAUBENSFRAGEN_VOR_DER_MENSA_STELLEN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.JUENGER): 2}},
            },
        )
        Action.objects.update_or_create(
            name="PCG programmieren",
            uuid=ActionIDs.PCG_PROGRAMMIEREN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.CAPTURE_THE_FLAG): 1}},
            },
        )
        Action.objects.update_or_create(
            name="Tischtennis trainieren",
            uuid=ActionIDs.TISCHTENNIS_TRAINIEREN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {
                    "produced_material": {str(StuffIDs.OLYMPIA_RANGLISTENPUNKTE): 1}
                },
            },
        )
        Action.objects.update_or_create(
            name="MyFitCoach programmieren/Andoid Emulator starten",
            uuid=ActionIDs.MFC_PROGRAMMIEREN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.MONEY): 10}},
            },
        )
        Action.objects.update_or_create(
            name="Issue bearbeiten",
            uuid=ActionIDs.ISSUE_BEARBEITEN,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.ISSUE): 1}},
            },
        )
        Action.objects.update_or_create(
            name="TTT um 10",
            uuid=ActionIDs.TTT_UM_10,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.CLAAS_VERSCHLAEFT): 1}},
            },
        )
        Action.objects.update_or_create(
            name="TTT um 10:30",
            uuid=ActionIDs.TTT_UM_10_30,
            defaults={
                "category": "PR",
                "application_duration": 20,
                "effect_duration": None,
                "conditions": {
                    "required_actions": None,
                    "prohibitive_actions": None,
                    "material": [],
                    "num_personnel": 1,
                    "lab_devices": None,
                    "area": None,
                    "role": [],
                },
                "results": {"produced_material": {str(StuffIDs.RETRO_PHOTO): 10}},
            },
        )

    @staticmethod
    def create_a_2_3():
        if not Exercise.objects.filter(frontend_id="django").exists():
            settings.ID_GENERATOR.codes_taken.append("django")
        else:
            Exercise.objects.get(frontend_id="django").delete()

        # I have no friggin idea why this is necessary, but it is (exercise deletion should cascade area and therefore patient deletion)
        if not PatientInstance.objects.filter(frontend_id=424242).exists():
            settings.ID_GENERATOR.codes_taken.append("424242")
        else:
            PatientInstance.objects.get(frontend_id=424242).delete()

        exercise = Exercise.createExercise()
        exercise.frontend_id = "django"
        area = Area.create_area(name="A-2.3", exercise=exercise, isPaused=False)
        patient_information = PatientInformation.objects.get(code=1004)

        patient, _ = PatientInstance.objects.update_or_create(
            frontend_id=424242,
            defaults={
                "name": "Sprint 10",
                "static_information": patient_information,
                "exercise": exercise,
                "area": area,
            },
        )
        Personnel.objects.update_or_create(
            name="Jojo",
            area=area,
        )
        Personnel.objects.update_or_create(
            name="Joshua",
            area=area,
        )
        Personnel.objects.update_or_create(
            name="Toni",
            area=area,
        )
        Personnel.objects.update_or_create(
            name="Claas",
            area=area,
        )


import csv
import re

from helpers.triage import Triage
from template.models import PatientInformation


def get_triage_from_string(string):
    switch = {"grün": Triage.GREEN, "rot": Triage.RED, "gelb": Triage.YELLOW}
    return switch.get(string, Triage.UNDEFINED)


def import_patients(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            triage = get_triage_from_string(row["PAK Info"].split(";")[0].strip())
            consecutiveUniqueNumber = int(
                re.sub("[^0-9]", "", row["PAK Info"].split(";")[1]) or -1
            )  # first half is interpreted as boolean and if it's false / undefined / not valid, -1 is saved as default value. Otherwise,
            # the number is extracted from the string

            biometrics = (
                row["Geschlecht"].strip()
                + "; "
                + row["Alter"].strip()
                + "; "
                + row["Biometrie"].strip()
            )

            PatientInformation.objects.update_or_create(
                code=row["Pat-Nr."].strip(),
                personal_details=row["Personalien"].strip(),
                injury=row["Verletzungen"].strip(),
                biometrics=biometrics,
                triage=triage,
                consecutive_unique_number=consecutiveUniqueNumber,
                mobility=row["Mobilität"].strip(),
                preexisting_illnesses=row["Vorerkrankungen"].strip(),
                permanent_medication=row["Dauer-Medikation"].strip(),
                current_case_history=row[
                    "Aktuelle Anamnese / Rettungsdienst-Übergabe"
                ].strip(),
                pretreatment=row["Vorbehandlung"].strip(),
                start_status=row["Start-Status"].strip(),
                start_location=row["Start-Ort"].strip(),
                op=row["OP / Interventions-Verlauf"].strip(),
            )
