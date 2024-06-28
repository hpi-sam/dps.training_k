import csv
import re
import uuid
from django.core.management.base import BaseCommand

from helpers.triage import Triage
from template.models import PatientInformation
from template.constants import ActionIDs


def get_triage_from_string(string):
    switch = {"grün": Triage.GREEN, "rot": Triage.RED, "gelb": Triage.YELLOW}
    return switch.get(string, Triage.UNDEFINED)


pretreatment_to_ActionIDs = {
    "Zugang": ActionIDs.IV_ZUGANG,
    "Nitrat": ActionIDs.NITRAT,
    "Wundversorgung": ActionIDs.WUNDVERSORGUNG,
    "VEL": ActionIDs.VOLLELEKTROLYT_500,
    "Analgetikum": ActionIDs.ANALGETIKUM,
    "AnalgetikumP": ActionIDs.ANALGETIKUM,
    "Sedativum": ActionIDs.SEDATIVUM,
    "Katecholamin": ActionIDs.KATECHOLAMIN,
    "Antikoagulanz": ActionIDs.ANTIKOAGULANZ,
    "Kortikosteroid": ActionIDs.KORTIKOSTEROID,
    "Narkotikum": ActionIDs.NARKOTIKUM,
    "künstlicher Atemweg": ActionIDs.TRACHEALTUBUS,
    "ZVK": ActionIDs.ZVK,
    "Glukose": ActionIDs.GLUCOSE_VERABREICHEN,
    "Glucose": ActionIDs.GLUCOSE_VERABREICHEN,
    "Antibiotikum": ActionIDs.ANTIBIOTIKUM,
    "Sauerstoff": ActionIDs.SAUERSTOFF_ANBRINGEN,
    "Beatmung": ActionIDs.BEATMUNGSGERAET_ANBRINGEN,
    "Rettungsdienst-Beatmung": None,
    "Rettungsdienst-Sauerstoff": None,
    "Rettungsdienst-Stifneck": None,
    "Rettungsdienst-Vacuum-Matratze": None,
    "Rettungsdienst-Extremitätenschiene": None,
}


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

            patient_information, _ = PatientInformation.objects.update_or_create(
                code=row["Pat-Nr."].strip(),
                personal_details=row["Personalien"].strip(),
                blood_type=row["Blutgruppe"].strip(),
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
            pretreatments_list = [
                pt.strip() for pt in patient_information.pretreatment.split(",")
            ]
            for pretreatment in pretreatments_list:
                if not pretreatment:
                    continue

                if (
                    pretreatment[-1] == "P"
                ):  # we don't distinguish between oral and intravenous medication
                    pretreatment = pretreatment[:-1]
                amount = re.match(r"(\d+x)", pretreatment)
                if amount:
                    amount = amount.group(1)
                    pretreatment = pretreatment.replace(amount, "")
                    amount = int(amount[:-1])
                else:
                    amount = 1
                translated_pretreatment = pretreatment_to_ActionIDs.get(pretreatment)
                if translated_pretreatment:
                    patient_information.pretreatment_action_templates[
                        str(translated_pretreatment)
                    ] = amount
            patient_information.save()


class Command(BaseCommand):
    help = "Imports patient data from a CSV file"

    def handle(self, *args, **options):
        import_patients("./data/patient_information.csv")  # path to the csv file
        self.stdout.write(self.style.SUCCESS("Successfully imported patient data"))
