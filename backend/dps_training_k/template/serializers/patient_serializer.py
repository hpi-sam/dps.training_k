from rest_framework import serializers
from template.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField()
    flow = serializers.SerializerMethodField()
    states = serializers.SerializerMethodField()
    transitions = serializers.SerializerMethodField()
    components = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            "info",
            "flow",
            "states",
            "transitions",
            "components",
        ]
        read_only = fields

    def get_info(self, obj):
        return obj.get("info")
    
    def get_flow(self, obj):
        return obj.get("flow")
    
    def get_states(self, obj):
        return obj.get("states")
    
    def get_transitions(self, obj):
        return obj.get("transitions")
    
    def get_components(self, obj):
        return obj.get("components")