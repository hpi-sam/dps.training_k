from django.db import models
from helpers.models import UUIDable
from django.contrib.postgres.fields import ArrayField
import json

class Action(UUIDable, models.Model):
    class Category(models.TextChoices):
        TREATMENT = "TR", "treatment"
        EXAMINATION = "EX", "examination"
        LAB = "LA", "lab"
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
    results = ArrayField(models.CharField(max_length=10), null=True, blank=True, default=None)

    def get_result(self, patient_state_data=None, area_materials=None):
        if self.category == Action.Category.TREATMENT:
            return self.treatment_result(patient_state_data)
        elif self.category == Action.Category.EXAMINATION:
            return self.examination_result(patient_state_data)
        elif self.category == Action.Category.LAB:
            return self.lab_result(area_materials)

    def treatment_result(self, patient_state):
        return "This is a treatment result"

    def examination_result(self, patient_state_data):
        result_string = f"{self.name} Ergebnis:"
        for key in self.results:
            result_string += f" {key}: {json.loads(patient_state_data)[key]}"
        return result_string

    def lab_result(self, area_materials):
        return "This is a lab result"

    def application_status(self, patient_instance, area):
        return True, None
