from rest_framework import serializers
from abc import ABC
import template.models.action as a


class ActionSerializer(serializers.ModelSerializer):
    applicationDuration = serializers.IntegerField(source="application_duration")
    effectDuration = serializers.IntegerField(source="effect_duration")

    class Meta:
        model = a.Action
        fields = [
            "actionName",
            "applicationDuration",
            "effectDuration",
        ]
        read_only_fields = fields


class ActionCheckSerializer(ABC):
    @property
    def data(self):
        return ActionSerializer(self.action).data + {
            "personnel": self.personnel_available_assigned_needed(),
            "material": self.material_available_assigned_needed(),
        }


class PatientInstanceActionCheckSerializer(ActionCheckSerializer):
    def __init__(self, action, patient_instance):
        self.action = action
        self.patient_instance = patient_instance

    def personnel_available_assigned_needed(self):
        return [
            {
                "name": "Beliebiges Personal",
                "available": self.patient_instance.personnel_available(),
                "assigned": self.patient_instance.personel_assigned(),
                "needed": self.action.personnel_count__needed(),
            }
        ]

    def material_available_assigned_needed(self):
        all_material = []
        for material_group in self.action.material_needed():
            for material in material_group:
                all_material.append(material)
        material_entries = []
        for material in all_material:
            material_entries.append(
                {
                    "name": material.name,
                    "available": self.patient_instance.material_available(material),
                    "assigned": self.patient_instance.material_assigned(material),
                    "needed": 1,
                }
            )
        return material_entries


class LabActionCheckSerializer(ActionCheckSerializer):
    def __init__(self, action, lab):
        self.action = action
        self.lab = lab

    def personnel_available_assigned_needed(self):
        return [
            {
                "name": "Beliebiges Personal",
                "available": self.lab.personnel_available(),
                "assigned": self.lab.personel_assigned(),
                "needed": self.action.personnel_count__needed(),
            }
        ]

    def material_available_assigned_needed(self):
        all_material = []
        for material_group in self.action.material_needed():
            for material in material_group:
                all_material.append(material)
        material_entries = []
        for material in all_material:
            material_entries.append(
                {
                    "name": material.name,
                    "available": self.lab.material_available(material),
                    "assigned": self.lab.material_assigned(material),
                    "needed": 1,
                }
            )
        return material_entries
