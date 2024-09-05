import os
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from template.models import Patient
from template.models import PatientInformation
from template.models import PatientState
from template.models import StateTransition

class Command(BaseCommand):
    help = "Import patients from json file"

    def handle(self, *args, **options):
        self.import_from_json()
        self.import_from_patient_states_model()
        return
    
    def import_from_json(self):
        file_path = os.path.join(settings.DATA_ROOT, "patients.json")
        if not os.path.exists(file_path):
            self.stderr.write(f"File {file_path} does not exist")
            return

        with open(file_path, "r") as file:
            patient_data_list = json.load(file)
        
        if isinstance(patient_data_list, list):
            for patient_data in patient_data_list:
                Patient.objects.update_or_create(
                    info=patient_data.get("info"),
                    flow=patient_data.get("flow"),
                    states=patient_data.get("states"),
                    transitions=patient_data.get("transitions"),
                    components=patient_data.get("components"),
                )
            self.stdout.write(self.style.SUCCESS("Successfully imported patients"))
        else:
            self.stderr.write("Unable to import patients")
        
        return
    
    def import_from_patient_states_model(self):
        patients_info = PatientInformation.objects.all().values()
        patients_state = PatientState.objects.all().values()
        state_transitions = StateTransition.objects.all().values()
        
        for patient_info in patients_info:
            initial_state_id = patient_info.get("start_status")
            info = {
                "code": patient_info.get("code"),
                "triage": patient_info.get("triage"),
                "sex": patient_info.get("biometrics"),
                "age": patient_info.get("biometrics"),
                "address": patient_info.get("personal_details"),
                # "blood_type": patient_info.get("blood_type"),
                "injury": patient_info.get("injury"),
                "biometrics": patient_info.get("biometrics"),
                "mobility": patient_info.get("mobility"),
                "preexistingIllnesses": patient_info.get("preexisting_illnesses"),
                "permanentMedication": patient_info.get("permanent_medication"),
                "currentCaseHistory": patient_info.get("current_case_history"),
                "pretreatment": patient_info.get("pretreatment"),
                # "pretreatment_action_templates": patient_info.get("pretreatment_action_templates"),
                # "start_status": patient_info.get("start_status"),
                # "start_location": patient_info.get("start_location"),
                # "op": patient_info.get("op"),
            }
            
            patient_states = PatientState.objects.filter(code=patient_info.get("code")).values()
            initial_state = patient_states.filter(state_id=initial_state_id).values()[0]
            
            states = []
            for patient_state in patient_states:
                state = {
                    "id": patient_state.get("state_id"),
                    "is_dead": patient_state.get("is_dead"),
                    "vital_signs": patient_state.get("vital_signs"),
                    "examination_codes": patient_state.get("examination_codes"),
                    # "special_events": patient_state.get("special_events"),
                }
                states.append(state)
            
            transitions_to_look_for = []
            flow = []
            for patient_state in patient_states:
                state_node = {
                    "id": patient_state.get("state_id"),
                    "type": "InitialState" if patient_state.get("state_id") == initial_state else "State",
                    "next": patient_state.get("transition"),
                }
                flow.append(state_node)
                transitions_to_look_for.append(patient_state.get("transition"))
            
            for transition in transitions_to_look_for:
                next = []
                transition_counter = 0
                key_counter = 0
                
                while transition is not None:
                    key = key_counter
                    value = transition.get("resulting_state")
                    next.append({
                        key: key,
                        value: value,
                    })
                    key_counter += 1
                    transition = transition.get("next_state_transition")
                    
                transition_node = {
                    "id": transition_counter,
                    "type": "Transition",
                    "transition": f"Transition {transition_counter}",
                    "next": next,
                }
                flow.append(transition_node)
                transition_counter += 1
                
            Patient.objects.update_or_create(
                info=info,
                flow=flow,
                states=states,
                transitions=[],
                components=[],
            )
            
        self.stdout.write(self.style.SUCCESS("Successfully imported old patients"))
        
        return