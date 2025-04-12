from rest_framework import serializers
from template.models import PatientState

class StateSerializer(serializers.Serializer):
    airway = serializers.SerializerMethodField()
    breathing = serializers.SerializerMethodField()
    circulation = serializers.SerializerMethodField()
    consciousness = serializers.SerializerMethodField()
    pupils = serializers.SerializerMethodField()
    psyche = serializers.SerializerMethodField()
    skin = serializers.SerializerMethodField()

    class Meta:
        model = PatientState
        fields = [
            "airway",
            "breathing",
            "circulation",
            "consciousness",
            "pupils",
            "psyche",
            "skin",
        ]
        read_only = fields

    def get_airway(self, obj):
        return obj.get("airway")

    def get_breathing(self, obj):
        return f"{obj.get('breathingRate')}, {obj.get('oxygenSaturation')}, {obj.get('oxygenSaturation')}, {obj.get('breathingSound')}, {obj.get('breathingLoudness')}"

    def get_circulation(self, obj):
        return f"{obj.get('heartRate')}, {obj.get('pulsePalpable')}, {obj.get('rivaRocci')}"

    def get_consciousness(self, obj):
        return obj.get("consciousness")

    def get_pupils(self, obj):
        return obj.get("pupils")

    def get_psyche(self, obj):
        return obj.get("psyche")

    def get_skin(self, obj):
        return f"{obj.get('skinFinding')}, {obj.get('skinDiscoloration')}"