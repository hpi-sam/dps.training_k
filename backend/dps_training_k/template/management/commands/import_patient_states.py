from django.core.management.base import BaseCommand
import csv, json
from template.models import PatientState, Subcondition
from django.conf import settings
import os
from template.constants import ActionIDs

CUSTOM_MAXINT = 100000 # doesn't matter, people shouldn't be doing the same thing 100000 times anyway

class Command(BaseCommand):
    help = "Populates the database with patient states."

    def handle(self, *args, **kwargs):
        self.create_subconditions()
        self.create_patient_phases()
        self.stdout.write(
            self.style.SUCCESS("Successfully added patient states to the database")
        )

    def create_subconditions(self):
        # corresponds to "Lyse"
        Subcondition.objects.update_or_create(
            name="keine Lyse",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.LYSE_VERARBREICHEN: 0},
        )
        Subcondition.objects.update_or_create(
            name="Lyse",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.LYSE_VERARBREICHEN: 1},
        )
        # corresponds to "4 EK´s"
        Subcondition.objects.update_or_create(
            name="0-3 EKs",
            upper_limit=3,
            lower_limit=0,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 0},
        )
        Subcondition.objects.update_or_create(
            name="4-inf EKs",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=4,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 4},
        )
        # corresponds to "Infusion"
        Subcondition.objects.update_or_create(
            name="0-999 Infusion",
            upper_limit=999,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="1000-1999 Infusion",
            upper_limit=1999,
            lower_limit=1000,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="2000-2999 Infusion",
            upper_limit=2999,
            lower_limit=2000,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="3000-inf Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=3000,
            fulfilling_measures={},
        )
        # corresponds to "2l Infusion"
        Subcondition.objects.update_or_create(
            name="0-1999 Infusion",
            upper_limit=1999,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="2000-inf Infusion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=2000,
            fulfilling_measures={},
        )
        # corresponds to "Thoraxdrainage/ Pleurapunktion"
        Subcondition.objects.update_or_create(
            name="keine Thoraxdrainage/ Pleurapunktion",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.THORAXDRAINAGE: 0, ActionIDs.PLEURAPUNKTION: 0},
        )
        Subcondition.objects.update_or_create(
            name="Thoraxdrainage/ Pleurapunktion",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.THORAXDRAINAGE: 1, ActionIDs.PLEURAPUNKTION: 1},
        )
        # corresponds to "Glucose"
        Subcondition.objects.update_or_create(
            name="keine Glucose",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.GLUCOSE_VERABREICHEN: 0},
        )
        Subcondition.objects.update_or_create(
            name="Glucose",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.GLUCOSE_VERABREICHEN: 1},
        )
        # corresponds to "Nitrat"
        Subcondition.objects.update_or_create(
            name="kein Nitrat",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.NITRAT: 0},
        )
        Subcondition.objects.update_or_create(
            name="Nitrat",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.NITRAT: 1},
        )
        # corresponds to O2
        Subcondition.objects.update_or_create(
            name="kein O2",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="O2",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "OP läuft / ist gelaufen" as well as "keine OP"
        Subcondition.objects.update_or_create(
            name="keine OP läuft / ist gelaufen",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="OP läuft / ist gelaufen",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "Analgesie"
        Subcondition.objects.update_or_create(
            name="keine Analgesie",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.ANALGETIKUM: 0},
        )
        Subcondition.objects.update_or_create(
            name="Analgesie",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.ANALGETIKUM: 1},
        )
        # corresponds to "O2 Inhalation"
        Subcondition.objects.update_or_create(
            name="O2 Inhalation",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="O2 Inhalation",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "CPAP"
        Subcondition.objects.update_or_create(
            name="kein CPAP",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="CPAP",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "Antiasthmatikum"
        Subcondition.objects.update_or_create(
            name="kein Antiasthmatikum",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.ANTIASTHMATIKUM: 0},
        )
        Subcondition.objects.update_or_create(
            name="Antiasthmatikum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.ANTIASTHMATIKUM: 1},
        )
        # corresponds to "Sedativum"
        Subcondition.objects.update_or_create(
            name="kein Sedativum",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.SEDATIVUM: 0},
        )
        Subcondition.objects.update_or_create(
            name="Sedativum",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.SEDATIVUM: 1},
        )
        # corresponds to "freie Atemwege"
        Subcondition.objects.update_or_create(
            name="keine freien Atemwege",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={},
        )
        Subcondition.objects.update_or_create(
            name="freie Atemwege",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={},
        )
        # corresponds to "EK´s"
        Subcondition.objects.update_or_create(
            name="0-1 EKs",
            upper_limit=1,
            lower_limit=0,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 0},
        )
        Subcondition.objects.update_or_create(
            name="2-3 EKs",
            upper_limit=3,
            lower_limit=2,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 2},
        )
        Subcondition.objects.update_or_create(
            name="4-5 EKs",
            upper_limit=5,
            lower_limit=4,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 4},
        )
        Subcondition.objects.update_or_create(
            name="6-inf EKs",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=6,
            fulfilling_measures={ActionIDs.ENTHROZYTENKONZENTRATE_ANWENDEN: 6},
        )
        # corresponds to "Beatmet"
        Subcondition.objects.update_or_create(
            name="Nicht beatmet",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.BEATMUNG: 0},
        )
        Subcondition.objects.update_or_create(
            name="Beatmet",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.BEATMUNG: 1},
        )
        # corresponds to Blutstillung
        Subcondition.objects.update_or_create(
            name="keine Blutstillung",
            upper_limit=0,
            lower_limit=0,
            fulfilling_measures={ActionIDs.CHIR_BLUTSTILLUNG: 0},
        )
        Subcondition.objects.update_or_create(
            name="Blutstillung",
            upper_limit=CUSTOM_MAXINT,
            lower_limit=1,
            fulfilling_measures={ActionIDs.CHIR_BLUTSTILLUNG: 1},
        )


    def create_patient_phases(self):
        for i in range(1001, 1002):
            filename = str(i) + "_tables.csv"
            # with open(filename, newline="", encoding="utf-8") as csvfile:

            base_dir = os.path.join(settings.DATA_ROOT, "patient_states/")
            filename = str(i) + "_transitions.csv"
            full_path = os.path.join(base_dir, filename)
            with open(full_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                csv_fields = []
                for field in next(
                    reader
                ):  # go through first line to get all field names
                    csv_fields.append(field)
                csv_fields = csv_fields[1:-1]  # remove "Status" and "Übergangstabelle"
                for row in reader:
                    row = [field.replace("|", "\n") for field in row]

                    state_id = int(row[0])
                    transition = None
                    data = []
                    i = 1
                    for field in csv_fields:
                        d = {field: row[i]}
                        i += 1
                        data.append(d)
                    data = json.dumps(data)
                    state_depth = int(row[0][-1])  # aka phase?
                    if state_depth == 0:
                        state_depth = 10
                    is_dead = state_id == 500 or state_id == 502
                    print(state_id)
                    print(data)
                    print(state_depth)
                    print(is_dead)

                    # PatientState.objects.create(
                    #     state_id=row[0],
                    #     transition=transition,
                    #     data=data,
                    #     state_depth=state_depth,
                    #     is_dead=is_dead,
                    # )


#TODO: can there be more than 10 states (phases) for a patient? i.e. 101 -> 151 -> ...
#TODO: can't get state_depth using modulo only, e.g. 101 is phase 0

#TODO: how do we check "freie Atemwege"? this doesn't depend on measures, instead its in the patient state data
#TODO: which action corresponds to "Infusion"?
#TODO: add action for Operation, then also add to corresponding Subcondition
#TODO: which action corresponds to "O2 Inhalation", same for O2?
#TODO: which action corresponds to "CPAP"?
#TODO: are there more "Blutstillungen" than "Chir. Blutstillung"?