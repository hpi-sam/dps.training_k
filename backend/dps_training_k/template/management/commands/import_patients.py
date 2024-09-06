import os
import json

from django.conf import settings
from django.core.management.base import BaseCommand

from template.models import Patient
from template.models import PatientInformation
from template.models import PatientState
from template.models import StateTransition
from template.models import LogicNode

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
        patients_info = list(PatientInformation.objects.all())
        
        for patient_info in patients_info:
            initial_state_id = patient_info.start_status
            info = {
                "code": patient_info.code,
                "triage": patient_info.triage,
                "sex": patient_info.biometrics,
                "age": patient_info.biometrics,
                "address": patient_info.personal_details,
                # "blood_type": patient_info.blood_type,
                "injury": patient_info.injury,
                "biometrics": patient_info.biometrics,
                "mobility": patient_info.mobility,
                "preexistingIllnesses": patient_info.preexisting_illnesses,
                "permanentMedication": patient_info.permanent_medication,
                "currentCaseHistory": patient_info.current_case_history,
                "pretreatment": patient_info.pretreatment,
                # "pretreatment_action_templates": patient_info.pretreatment_action_templates,
                # "start_status": patient_info.start_status,
                # "start_location": patient_info.start_location,
                # "op": patient_info.op,
            }
            
            patient_states = list(PatientState.objects.filter(code=patient_info.code))
            
            states = []
            for patient_state in patient_states:
                state = {
                    "id": "State-" + str(patient_state.state_id),
                    "is_dead": patient_state.is_dead,
                    "vital_signs": patient_state.vital_signs,
                    "examination_codes": patient_state.examination_codes,
                    # "special_events": patient_state.special_events,
                }
                states.append(state)
            
            transitions_to_look_for = []
            flow = []
            for patient_state in patient_states:
                state_node = {
                    "id": "State-" + str(patient_state.state_id),
                    "type": "InitialState" if patient_state.state_id == initial_state_id else "State",
                    "next": "Transition-" + str(patient_state.transition.id),
                }
                flow.append(state_node)
                
                if patient_state.transition and (patient_state.transition not in transitions_to_look_for):
                    transitions_to_look_for.append(patient_state.transition)
            
            transitions = []
            for transition in transitions_to_look_for:
                resulting_state_id = transition.resulting_state.state_id if transition.resulting_state is not None else None
                next_transition_id = transition.next_state_transition.id if transition.next_state_transition is not None else None
                
                next = []
                output_nodes = []
                key_counter = 1
                while next_transition_id is not None:
                    next.append({
                        'key': str(key_counter),
                        'value': "State-" + str(resulting_state_id),
                    })
                    output_nodes.append({
                        "id": "Transition-" + str(transition.id) + "-Out-" + str(key_counter),
                        "type": "Output",
                        "key": str(key_counter),
                    })
                    key_counter += 1
                    if StateTransition.objects.get(id=next_transition_id).resulting_state is not None:
                        resulting_state_id = StateTransition.objects.get(id=next_transition_id).resulting_state.state_id
                    else:
                        resulting_state_id = None
                    if StateTransition.objects.get(id=next_transition_id).next_state_transition is not None:
                        next_transition_id = StateTransition.objects.get(id=next_transition_id).next_state_transition.id
                    else:
                        next_transition_id = None
                    
                transition_node = {
                    "id": "Transition-" + str(transition.id),
                    "type": "Transition",
                    "transition": "Transition-" + str(transition.id),
                    "next": next,
                }
                flow.append(transition_node)
                
                new_transition = self.import_transition(transition, output_nodes)
                transitions.append(new_transition)
                
            Patient.objects.update_or_create(
                info=info,
                flow=flow,
                states=states,
                transitions=transitions,
                components=[],
            )
            
        self.stdout.write(self.style.SUCCESS("Successfully imported old patients"))
        
        return
    
    def import_transition(self, transition, output_nodes):
        transition_flow = []
        transition_flow.append({
            "id": "Transition-" + str(transition.id) + "-In",
            "type": "Input",
            "key": "in",
            "next": "",
        })
        transition_flow.extend(output_nodes)
        
        return {
            "id": "Transition-" + str(transition.id),
            "flow": transition_flow,
        }