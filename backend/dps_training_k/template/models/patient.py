from django.db import models
import logging

logger = logging.getLogger(__name__)

class Patient(models.Model):
    info = models.JSONField()
    flow = models.JSONField()
    states = models.JSONField()
    transitions = models.JSONField()
    components = models.JSONField()

    def __str__(self):
        return f"Patient {self.info.get('code', 'Unknown')}"
    
    def get_node(self, node_id, flow=None):
        if flow is None:
            flow = self.flow
        return next((n for n in flow if n.get('id') == node_id), None)

    def get_state(self, state_id):
        return next((s for s in self.states if s.get('id') == state_id), None)
    
    def get_transition(self, transition_id):
        return next((t for t in self.transitions if t.get('id') == transition_id), None)
    
    def get_input_node(self, transition_id):
        transition = self.get_transition(transition_id)
        return next((f for f in transition.get('flow', []) if f.get('type') == "Input"), None)

    def get_initial_state_id(self):
        return next((n.get('id') for n in self.flow if n.get('type') == "InitialState"), None)
    
    def is_dead(self, state_id):
        state = self.get_state(state_id)
        return state.get('isDead', False)
    
    def is_final_state(self, state_id):
        state = self.get_state(state_id)
        return next((n for n in self.flow if n.get('id') == state.get('id')), {}).get('next') == None
                
    def get_next_state_id(self, state_id, check_action, check_material):
        logger.info(f"Getting next state for state {state_id}")
        
        state = self.get_state(state_id)
        logger.info(f"State: {state}")
        
        node = self.get_node(state.get('id'))
        logger.info(f"Node: {node}")
        
        transition_flow_id = node.get('next')
        transition_node = self.get_node(transition_flow_id)
        logger.info(f"Transition node: {transition_node}")
        
        transition_id = transition_node.get('transition')
        transition = self.get_transition(transition_id)
        logger.info(f"Transition: {transition}")
        
        current_node_id = self.get_input_node(transition_id).get('next')
        current_node = self.get_node(current_node_id, transition.get('flow'))
        logger.info(f"Current node: {current_node}")
        
        while current_node and current_node.get('type') != "Output":
            logger.info(f"Current node type: {current_node.get('type')}")
            condition_is_met = False
            if current_node.get('type') == "Action":
                condition_is_met = check_action(current_node.get('action'), current_node.get('quantity'))
            elif current_node.get('type') == "Material":
                condition_is_met = check_material(current_node.get('material'), current_node.get('quantity'))
                
            logger.info(f"Condition is met: {condition_is_met}")
            if condition_is_met:
                current_node_id = current_node.get('next').get('true')
            else:
                current_node_id = current_node.get('next').get('false')
            
            current_node = self.get_node(current_node_id, self.get_transition(transition_id).get('flow'))
            logger.info(f"Current node: {current_node}")
        
        next_state_id = next((n.get('value') for n in transition_node.get('next', []) if n.get('key') == current_node.get('key')), None)
        logger.info(f"Next state id: {next_state_id}")
        return next_state_id
    
    '''
    def check_action(action, quantity, patient_instance):
        logger.info(f"Checking action {action} with quantity {quantity}")
        from game.models import ActionInstanceState
        # Fetch all action instances related to the patient
        action_instances = patient_instance.actioninstance_set.select_related("template").all()

        # Filter action instances to include only those in success states
        success_action_instances = [
            ai for ai in action_instances 
            if ai.current_state.name in ActionInstanceState.success_states() and str(ai.template.uuid) == action
        ]
        logger.info(f"Success action instances: {success_action_instances}")

        # Count the number of instances of the specified action in success states
        action_count = len(success_action_instances)
        logger.info(f"Action count: {action_count}")
        
        return action_count >= quantity
    
    def check_material(self, material, quantity):
        return True
    '''