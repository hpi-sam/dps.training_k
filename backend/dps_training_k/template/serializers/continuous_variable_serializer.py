import re

from django.db.models import Q
from rest_framework import serializers

from game.models import PatientInstance, Owner
from template.models.continuous_variable import ContinuousVariable


def _extract_spo2(vital_signs):
    """Extracts the SpO2 value from a vital signs text."""
    return int(re.search(r"SpO2:\s*(\d+)", vital_signs["Breathing"]).group(1))


def _extract_bpm(vital_signs):
    """Extracts the heart rate value from a vital signs text."""
    return int(re.search(r"Herzfreq:\s*(\d+)", vital_signs["Circulation"]).group(1))


def _check_subset(condition_items, completed_items):
    """Generic method to check if all given condition items are fulfilled by being within the completed_items set."""
    if not condition_items:
        return True

    for item_group in condition_items:
        if isinstance(item_group, str):
            item_group = [item_group]
        if set(item_group).issubset(completed_items):
            return True
    return False


class ContinuousVariableSerializer(serializers.ModelSerializer):
    def __init__(self, patient_instance, **kwargs):
        super().__init__(**kwargs)
        if isinstance(patient_instance, PatientInstance):
            self.patient_instance = patient_instance
        else:
            raise TypeError(
                f"Expected 'patient_instance' to be of type PatientInstance. Got {type(patient_instance).__name__} instead."
            )

    @property
    def data(self):
        """Constructs the serialized data, including phase change time and continuous variables."""
        time_until_phase_change = self._get_time_until_phase_change()
        continuous_variables = self.continuous_variables()

        return {
            "timeUntilPhaseChange": time_until_phase_change,
            "continuousVariables": continuous_variables if continuous_variables else [],
        }

    def _get_time_until_phase_change(self):
        """Returns the time until the next phase change event, or 0 if none is scheduled."""
        phase_change_event_owners = Owner.objects.filter(
            Q(patient_owner=self.patient_instance)
            & Q(event__method_name="execute_state_change")
        )
        if phase_change_event_owners.exists():
            phase_change_event = (
                phase_change_event_owners.order_by("event__end_date").last().event
            )
            return phase_change_event.get_time_until_completion(self.patient_instance)
        return 0

    def continuous_variables(self):
        """Returns a list of continuous variable data for the patient."""
        future_state = self.patient_instance.next_state()
        if not future_state:
            return []

        variables = ContinuousVariable.objects.all()

        result = []
        for variable in variables:
            current, target = self._get_values(variable.name, future_state)
            function, var_hash = self._get_applicable_function(variable)
            var_hash = hash((var_hash, current, target))

            result.append(
                {
                    "name": variable.name,
                    "current": current,
                    "target": target,
                    "function": function,
                    "hash": var_hash,
                }
            )
        return result

    def _get_values(self, variable_name, future_state):
        match variable_name:
            case ContinuousVariable.Variable.SPO2:
                fun = _extract_spo2
            case ContinuousVariable.Variable.HEART_RATE:
                fun = _extract_bpm
            case _:
                raise TypeError(
                    f"Did not find values for given continuous variable {variable_name}."
                )

        return fun(self.patient_instance.patient_state.vital_signs), fun(
            future_state.vital_signs
        )

    def _flatten(self, lst):
        """Helper function to recursively flatten a list"""
        if isinstance(lst, list):
            return tuple(item for sublist in lst for item in self._flatten(sublist))
        return (lst,)

    def _get_applicable_function(self, variable):
        completed_action_uuids = {
            str(action.uuid)
            for action in self.patient_instance.get_completed_action_types()
        }
        completed_material_uuids = {
            str(material.template.uuid)
            for material in self.patient_instance.materialinstance_set.all()
        }

        for exception in variable.exceptions:
            function = exception["function"]
            actions = (
                self._flatten(exception["actions"]) if exception["actions"] else ()
            )
            materials = (
                self._flatten(exception["materials"]) if exception["materials"] else ()
            )

            if _check_subset(actions, completed_action_uuids) and _check_subset(
                materials, completed_material_uuids
            ):
                return function, hash((function, actions, materials))
        return variable.function, hash(variable.function)
