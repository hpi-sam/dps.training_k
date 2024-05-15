import csv
import re

from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Imports patient data from a CSV file"

    def handle(self, *args, **options):
        import_patients("./data/patient_information.csv")  # path to the csv file
        self.stdout.write(self.style.SUCCESS("Successfully imported patient data"))
