from rest_framework import serializers
from game.models import PatientState


class StateSerializer(serializers.Serializer):
    phaseNumber = serializers.IntegerField(source="current_phase", read_only=True)
    airway = serializers.CharField(source="data.airway", read_only=True)
    breathing = serializers.CharField(source="data.breathing", read_only=True)
    circulation = serializers.CharField(source="data.circulation", read_only=True)
    consciousness = serializers.CharField(source="data.consciousness", read_only=True)
    pupils = serializers.CharField(source="data.pupils", read_only=True)
    psyche = serializers.CharField(source="data.psyche", read_only=True)
    skin = serializers.CharField(source="data.skin", read_only=True)

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
