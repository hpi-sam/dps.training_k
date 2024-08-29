from django.db import models

class Patient(models.Model):
    info = models.JSONField()
    flow = models.JSONField()
    states = models.JSONField()
    transitions = models.JSONField()
    components = models.JSONField()

    def __str__(self):
        return f"Patient {self.info.get('code', 'Unknown')}"

    def get_state(self, state_id):
        for state in self.states:
            if state.get('id') == state_id:
                return state
        return None

    def get_initial_state_id(self):
        for node in self.flow:
            if node.get('type') == "InitialState":
                return node.get('id')
        return None
    
    def is_dead(self, state_id):
        state = self.get_state(state_id)
        return state.get('isDead', False)
    
    def is_final_state(self, state_id):
        state = self.get_state(state_id)
        for node in self.flow:
            if node.get('id') == state.get('id'):
                return node.get('next') == None
        return False
    
    '''
    getNextState(currentState) {
	transitionId = flow.find(id === currentState.next).transition
	transition = transitions.find(id === transitionId)
	currentNodeId = transition.flow.find(type === "Input").next
	currentNode = transitions.find(id === currentNodeId)
	while (currentNode.type != "Output") {
		if (currentNode.type === "Action") {
			currentNodeId = checkAction(currentNode.action, currentNode.quantity)
				? currentNode.true
				: currentNode.false
		}
		if (currentNode.type === "Material") {
			currentNodeId = checkMaterial(currentNode.material, currentNode.quantity)
				? currentNode.true
				: currentNode.false
		}
		currentNode = transitions.find(id === currentNodeId)
	}
	nextStateId = transition.next.find(key === currentNode.key)
	nextState = states.find(id === nextStateId)
	return nextState
    '''
                
    def get_next_state_id(self, state_id):
        state = self.get_state(state_id)
        if not state:
            return None
        
        for node in self.flow:
            if node.get('id') == state.get('id'):
                transition_id = node.get('next')
                transition = next((t for t in self.transitions if t.get('id') == transition_id), None)
                if not transition:
                    return None
                
                current_node_id = next((f.get('next') for f in transition.get('flow', []) if f.get('type') == "Input"), None)
                current_node = next((t for t in self.transitions if t.get('id') == current_node_id), None)
                
                while current_node and current_node.get('type') != "Output":
                    if current_node.get('type') == "Action":
                        current_node_id = current_node.get('true') if self.check_action(current_node.get('action'), current_node.get('quantity')) else current_node.get('false')
                    elif current_node.get('type') == "Material":
                        current_node_id = current_node.get('true') if self.check_material(current_node.get('material'), current_node.get('quantity')) else current_node.get('false')
                    
                    current_node = next((t for t in self.transitions if t.get('id') == current_node_id), None)
                
                next_state_id = next((n.get('id') for n in transition.get('next', []) if n.get('key') == current_node.get('key')), None)
                return next_state_id
        
        return None
    
    def check_action(self, action, quantity):
        """
        Check if there are at least 'quantity' of action instances in the success states.
        
        :param action: The action to check.
        :param quantity: The required quantity.
        :return: True if there are at least 'quantity' of action instances in success states, False otherwise.
        """
        from game.models import ActionInstanceState
        # Fetch all action instances related to the patient
        action_instances = self.actioninstance_set.select_related("template").all()

        # Filter action instances to include only those in success states
        success_action_instances = [
            ai for ai in action_instances 
            if ai.current_state.name in ActionInstanceState.success_states() and str(ai.template.uuid) == action
        ]

        # Count the number of instances of the specified action in success states
        action_count = len(success_action_instances)

        # Check if the count meets or exceeds the required quantity
        return action_count >= quantity
    
    def check_material(self, material, quantity):
        return True