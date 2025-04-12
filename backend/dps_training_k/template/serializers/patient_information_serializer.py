from rest_framework import serializers
from template.models import Patient


class PatientInformationSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    injury = serializers.SerializerMethodField()
    biometrics = serializers.SerializerMethodField()
    triage = serializers.SerializerMethodField()
    mobility = serializers.SerializerMethodField()
    preexistingIllnesses = serializers.SerializerMethodField()
    permanentMedication = serializers.SerializerMethodField()
    currentCaseHistory = serializers.SerializerMethodField()
    pretreatment = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "code",
            "injury",
            "biometrics",
            "triage",
            "mobility",
            "preexistingIllnesses",
            "permanentMedication",
            "currentCaseHistory",
            "pretreatment",
        ]
        read_only = fields

    def get_code(self, obj):
        return obj.get("info").get("code")

    def get_injury(self, obj):
        return obj.get("info").get("injury")

    def get_biometrics(self, obj):
        return obj.get("info").get("biometrics")

    def get_triage(self, obj):
        return obj.get("info").get("triage")

    def get_mobility(self, obj):
        return obj.get("info").get("mobility")
    
    def get_preexistingIllnesses(self, obj):
        return obj.get("info").get("preexistingIllnesses")
    
    def get_permanentMedication(self, obj):
        return obj.get("info").get("permanentMedication")
    
    def get_currentCaseHistory(self, obj):
        return obj.get("info").get("currentCaseHistory")

    def get_pretreatment(self, obj):
        return obj.get("info").get("pretreatment")