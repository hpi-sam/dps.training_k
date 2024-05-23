from rest_framework import serializers
from template.models import PatientState
import json

class StateSerializer(serializers.Serializer):
    airway = serializers.SerializerMethodField()
    breathing = serializers.SerializerMethodField()
    circulation = serializers.SerializerMethodField()
    consciousness = serializers.SerializerMethodField()
    pupils = serializers.SerializerMethodField()
    psyche = serializers.SerializerMethodField()
    skin = serializers.SerializerMethodField()
    # airway = serializers.CharField(source="vital_signs.Airway")
    # breathing = serializers.CharField(source="vital_signs.Breathing")
    # circulation = serializers.CharField(source="vital_signs.Circulation")
    # consciousness = serializers.CharField(source="vital_signs.Bewusstsein")
    # pupils = serializers.CharField(source="vital_signs.Pupillen")
    # psyche = serializers.CharField(source="vital_signs.Psyche")
    # skin = serializers.CharField(source="vital_signs.Haut")

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
        return json.loads(obj.vital_signs).get('Airway', None)
    def get_breathing(self, obj):
        return json.loads(obj.vital_signs).get('Breathing', None)
    def get_circulation(self, obj):
        return json.loads(obj.vital_signs).get('Circulation', None)
    def get_consciousness(self, obj):
        return json.loads(obj.vital_signs).get('Bewusstsein', None)
    def get_pupils(self, obj):
        return json.loads(obj.vital_signs).get('Pupillen', None)
    def get_psyche(self, obj):
        return json.loads(obj.vital_signs).get('Psyche', None)
    def get_skin(self, obj):
        return json.loads(obj.vital_signs).get('Haut', None)
