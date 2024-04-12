class ActionsQueueable:
    def register_to_queue(self, obj):
        # stub for future queueing logic
        pass

    # ToDo: verify with wlan
    def start_next_action(self):
        queue = self.action_instances.filter(
            state__name__eq=ActionInstanceStateName.PLANNED
        )
        while not queue[0].try_action():
            queue.pop(0)
