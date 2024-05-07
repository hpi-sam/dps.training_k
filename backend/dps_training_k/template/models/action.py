from django.db import models
from .material import Material
from helpers.models import UUIDable
import json, uuid


class Action(UUIDable, models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        LAB = "LA", "lab"
        PRODUCTION = "PR", "production"
        OTHER = "OT", "other"

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(choices=Category.choices, max_length=2)
    application_duration = models.IntegerField(
        default=10,
        help_text="Duration in seconds in realtime. Might be scaled by external factors.",
    )
    effect_duration = models.IntegerField(
        default=None,
        null=True,
        help_text="Effect duration in seconds in realtime. Might be scaled by external factors.",
    )
    conditions = models.JSONField(null=True, blank=True, default=None)
    results = models.JSONField(null=True, blank=True, default=None)

    def produced_resources(self):
        if not "produced_materials" in json.loads(self.results):
            return None
        resources = json.loads(self.results)["produced_materials"]
        resources = {
            Material.objects.get(uuid=uuid.UUID(key)): amount
            for key, amount in resources.items()
        }
        return resources

    def get_result(self, patient_state_data=None, area_materials=None):
        if self.category == Action.Category.TREATMENT:
            return self.treatment_result(patient_state_data)
        elif self.category == Action.Category.EXAMINATION:
            return self.examination_result(patient_state_data)
        elif self.category == Action.Category.LAB:
            return self.lab_result(area_materials)
        elif self.category == Action.Category.PRODUCTION:
            return self.production_result()

    def treatment_result(self, patient_state):
        return f"Behandlung {self.name} wurde durchgeführt"

    def examination_result(self, patient_state_data):
        result_string = f"{self.name} Ergebnis:"
        # iterate through result map
        results = json.loads(self.results)
        for key, values in results.items():
            # find correct result code for this patient
            result_code = json.loads(patient_state_data)[key]
            # find string value corresponding to result code
            found = False
            for value in values:
                if result_code in value:
                    result_string += f" {key}: {value[result_code]}"
                    found = True
            if not found:
                raise ValueError(
                    "Examination result: Couldn't find corresponding value for result code"
                )

        return result_string

    def production_result(self):
        return f"{self.name} wurde durchgeführt"

    def lab_result(self, area_materials):
        return "This is a lab result"

    def application_status(self, patient_instance, area, material_availabilities):
        return True, None
