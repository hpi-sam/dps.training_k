from abc import ABC

from rest_framework import serializers

import template.models.action as a


class ActionSerializer(serializers.ModelSerializer):
    actionName = serializers.CharField(source="name")
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
        data = ActionSerializer(self.action).data

        personnel_available_assigned_needed = self.personnel_available_assigned_needed()
        if personnel_available_assigned_needed:
            data.update({"personnel": personnel_available_assigned_needed})

        material_available_assigned_needed = self.material_available_assigned_needed()
        if material_available_assigned_needed:
            data.update({"material": material_available_assigned_needed})

        required_actions = self.required_actions()
        if required_actions:
            data.update({"requiredActions": required_actions})

        prohibitive_actions = self.prohibitive_actions()
        if prohibitive_actions:
            data.update({"prohibitiveActions": prohibitive_actions})

        return {"actionCheck": data}


class PatientInstanceActionCheckSerializer(ActionCheckSerializer):
    def __init__(self, action, patient_instance):
        self.action = action
        self.patient_instance = patient_instance

    def personnel_available_assigned_needed(self):
        return [
            {
                "name": "Beliebiges Personal",
                "available": len(self.patient_instance.personnel_available()),
                "assigned": len(self.patient_instance.personnel_assigned()),
                "needed": self.action.personnel_count_needed(),
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
                    "available": len(
                        self.patient_instance.material_available(material)
                    ),
                    "assigned": len(self.patient_instance.material_assigned(material)),
                    "needed": 1,
                }
            )
        return material_entries

    def required_actions(self):
        required_actions = self.action.required_actions()
        applied_actions = self.patient_instance.get_completed_action_types()
        single_actions = []
        group_actions = []
        for required_action_group in required_actions:
            if len(required_action_group) > 1:
                required_action_group_names = []
                for action in required_action_group:
                    if action not in applied_actions:
                        required_action_group_names.append(action.name)
                group_actions.append(
                    {"groupName": "", "actions": required_action_group_names}
                )
            else:
                if required_action_group[0] not in applied_actions:
                    single_actions.append(required_action_group[0].name)
        return {
            "singleActions": single_actions,
            "actionGroups": group_actions,
        }

    def prohibitive_actions(self):
        from game.models import ActionInstance

        applied_action_instances = ActionInstance.get_potentially_prohibiting_action_instances(
            self.patient_instance, self.patient_instance.lab
        )
        applied_actions = {
            action_instance.template for action_instance in applied_action_instances
        }
        prohibitive_actions = []
        for action in self.action.prohibitive_actions():
            if action[0] in applied_actions:
                prohibitive_actions.append(action[0].name)
        return prohibitive_actions


class LabActionCheckSerializer(ActionCheckSerializer):
    def __init__(self, action, lab, patient_instance):
        self.action = action
        self.lab = lab
        self.patient_instance = patient_instance

    def personnel_available_assigned_needed(self):
        if not self.action.personnel_count_needed():
            return []
        return [
            {
                "name": "Beliebiges Personal",
                "available": len(self.lab.personnel_available()),
                "assigned": len(self.lab.personnel_assigned()),
                "needed": self.action.personnel_count_needed(),
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
                    "available": len(self.lab.material_available(material)),
                    "assigned": len(self.lab.material_assigned(material)),
                    "needed": 1,
                }
            )
        return material_entries

    def required_actions(self):
        required_actions = self.action.required_actions()
        applied_actions = self.lab.get_completed_action_types()
        applied_actions = (
            applied_actions | self.patient_instance.get_completed_action_types()
        )
        single_actions = []
        group_actions = []
        for required_action_group in required_actions:
            if len(required_action_group) > 1:
                required_action_group_names = []
                for action in required_action_group:
                    if action not in applied_actions:
                        required_action_group_names.append(action.name)
                group_actions.append(
                    {
                        "groupName": "",
                        "actions": required_action_group_names,
                    }
                )
            else:
                if required_action_group[0] not in applied_actions:
                    single_actions.append(required_action_group[0].name)
        return {
            "singleActions": single_actions,
            "actionGroups": group_actions,
        }

    def prohibitive_actions(self):
        from game.models import ActionInstance

        applied_action_instances = ActionInstance.get_potentially_prohibiting_action_instances(
            self.patient_instance, self.lab
        )
        applied_actions = {
            action_instance.template for action_instance in applied_action_instances
        }
        prohibitive_actions = []
        for action in self.action.prohibitive_actions():
            if action[0] in applied_actions:
                prohibitive_actions.append(action[0].name)
        return prohibitive_actions
