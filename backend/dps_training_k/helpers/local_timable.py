from django.utils import timezone


class LocalTimeable:
    # ToDo: Replace with actual logic when implementing the scalable local time system
    def get_local_time(self):
        return timezone.now().timestamp()
