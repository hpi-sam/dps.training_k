class ActionsQueueable:
    def register_to_queue(self, obj):
        # stub for future queueing logic
        pass

    def remove_from_queue(self, obj):
        # stub for future queueing logic
        pass

    def start_next_action(self):
        queue = self.action_instances.filter(
            state__name__in=[
                ActionInstanceStateName.PLANNED,
                ActionInstanceStateName.ON_HOLD,
            ]
        )
        while queue and not queue[0].try_action():
            queue.pop()
