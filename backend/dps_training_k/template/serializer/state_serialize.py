from rest_framework import serializers
from template.models import PatientState


class StateSerializer(serializers.Serializer):
    phaseNumber = serializers.IntegerField(source="current_phase")
    airway = serializers.CharField(source="data.airway")
    breathing = serializers.CharField(source="data.breathing")
    circulation = serializers.CharField(source="data.circulation")
    consciousness = serializers.CharField(source="data.consciousness")
    pupils = serializers.CharField(source="data.pupils")
    psyche = serializers.CharField(source="data.psyche")
    skin = serializers.CharField(source="data.skin")

    class Meta:
        model = PatientState
        fields = [
            "phaseNumber",
            "airway",
            "breathing",
            "circulation",
            "consciousness",
            "pupils",
            "psyche",
            "skin",
        ]
        read_only = fields
