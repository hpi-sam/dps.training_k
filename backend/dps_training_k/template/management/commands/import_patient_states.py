from django.core.management.base import BaseCommand
import csv, json
from template.models import PatientState
from django.conf import settings
import os

class Command(BaseCommand):
    help = "Populates the database with patient states."

    def handle(self, *args, **kwargs):
        self.create_patient_phases()
        self.stdout.write(self.style.SUCCESS("Successfully added patient states to the database"))

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
                for field in next(reader): # go through first line to get all field names
                    csv_fields.append(field)
                csv_fields = csv_fields[1:-1] # remove "Status" and "Übergangstabelle"
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
