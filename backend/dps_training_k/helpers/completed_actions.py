
class CompletedActionsMixin:
    def get_completed_action_types(self):
        from game.models import ActionInstanceState
        action_instances = self.actioninstance_set.select_related("template").all()
        applied_actions = set()
        for action_instance in action_instances:
            if action_instance.current_state.name in ActionInstanceState.completion_states():
                applied_actions.add(action_instance.template)
        return applied_actions