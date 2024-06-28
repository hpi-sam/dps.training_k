import uuid
from django.db import models
from helpers.triage import Triage
from .action import Action


class PatientInformation(models.Model):
    """extracted from original data in ./data/patient_information.csv"""

    code = models.IntegerField(unique=True, help_text="Sensen Code")  # Pat-Nr.
    personal_details = models.CharField(max_length=300, default="-")  # Personalien
    blood_type = models.CharField(max_length=1, default="-")  # Blutgruppe
    injury = models.CharField(max_length=300, default="-")  # Verletzungen
    biometrics = models.CharField(
        max_length=300, default="-"
    )  # Geschlecht; Alter; Biometrie
    triage = models.CharField(
        choices=Triage.choices,
        default=Triage.UNDEFINED,
    )  # PAK Info erster Teil
    consecutive_unique_number = models.IntegerField(
        default=-1
    )  # PAK Info zweiter Teil eineindeutige Nummer (nicht bei jedem Patienten vorhanden → nicht unique)
    mobility = models.CharField(max_length=100, default="-")  # Mobilität
    preexisting_illnesses = models.CharField(
        max_length=300, default="-"
    )  # Vorerkrankungen
    permanent_medication = models.CharField(
        max_length=300, default="-"
    )  # Dauer-Medikation
    current_case_history = models.CharField(
        max_length=300, default="-"
    )  # Aktuelle Anamnese / Rettungsdienst-Übergabe
    pretreatment = models.CharField(max_length=300, default="-")  # Vorbehandlung
    pretreatment_action_templates = models.JSONField(default=dict)
    # internal information
    start_status = models.IntegerField(default=-1)  # Start-Status
    start_location = models.CharField(max_length=100, default="-")  # Start-Ort
    op = models.CharField(max_length=300, default="-")  # OP / Interventions-Verlauf
    """Step by step description of the operation/intervention process. Each step is separated by a | symbol."""

    @property
    def examination_codes(self):
        return {"Blutgruppe": self.blood_type}

    def get_pretreatments(self):
        for key, amount in self.pretreatment_action_templates.items():
            print(key)
        return {
            Action.objects.get(uuid=uuid.UUID(key)): amount
            for key, amount in self.pretreatment_action_templates.items()
        }
