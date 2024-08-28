import csv
import os
import re
import json
from copy import deepcopy

from django.conf import settings
from django.core.management.base import BaseCommand

from template.models import Patient

class Command(BaseCommand):
    help = "Import patients from json file"

    def handle(self, *args, **options):
        self.stdout.write("Importing patients")
        file_path = os.path.join(settings.DATA_ROOT, "patients.json")
        if not os.path.exists(file_path):
            self.stderr.write(f"File {file_path} does not exist")
            return

        with open(file_path, "r") as file:
            patient_data_list = json.load(file)
        
        # Ensure patient_data_list is a list
        if isinstance(patient_data_list, list):
            for patient_data in patient_data_list:
                Patient.objects.update_or_create(
                    info=patient_data.get("info"),
                    flow=patient_data.get("flow"),
                    states=patient_data.get("states"),
                    transitions=patient_data.get("transitions"),
                    components=patient_data.get("components"),
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported patients"))
        else:
            self.stderr.write("Unable to import patients")
        
        return