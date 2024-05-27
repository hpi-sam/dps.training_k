from rest_framework import serializers
from template.models import PatientState

class StateSerializer(serializers.Serializer):
    airway = serializers.CharField(source="vital_signs.Airway")
    breathing = serializers.CharField(source="vital_signs.Breathing")
    circulation = serializers.CharField(source="vital_signs.Circulation")
    consciousness = serializers.CharField(source="vital_signs.Bewusstsein")
    pupils = serializers.CharField(source="vital_signs.Pupillen")
    psyche = serializers.CharField(source="vital_signs.Psyche")
    skin = serializers.CharField(source="vital_signs.Haut")

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
    