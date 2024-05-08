from rest_framework import serializers
from template.models import PatientInformation


class PatientInformationSerializer(serializers.ModelSerializer):
    personalDetails = serializers.CharField(source="personal_details")
    consecutiveUniqueNumber = serializers.CharField(source="consecutive_unique_number")
    preexistingIllnesses = serializers.CharField(source="preexisting_illnesses")
    permanentMedication = serializers.CharField(source="permanent_medication")
    currentCaseHistory = serializers.CharField(source="current_case_history")

    class Meta:
        model = PatientInformation
        fields = [
            "code",
            "personalDetails",
            "injury",
            "biometrics",
            "triage",
            "consecutiveUniqueNumber",
            "mobility",
            "preexistingIllnesses",
            "permanentMedication",
            "currentCaseHistory",
            "pretreatment",
        ]
        read_only = fields
