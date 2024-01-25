from abc import ABC, abstractmethod
from channels.generic.websocket import JsonWebsocketConsumer


class AbstractConsumer(JsonWebsocketConsumer, ABC):
    """
    Base consumer to be used as an abstract class, preparing some shared behaviour, but never to
    be used directly.
    """

    class FailureCodes:
        UNKNOWN = 0

    class ClosureCodes:
        UNKNOWN = 0

    class OutgoingMessageTypes:
        PHASE_CHANGE = "patient.phaseChange"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = ""

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self, close_code):
        pass  # Add any cleanup here

    def receive_json(self, content):
        self.dispatch_request(content)

    def dispatch_request(self, content):
        request_type = content.get("type")
        if request_type:
            self.handle_request(request_type, content)
        else:
            self.send_json({"error": "Invalid request type"})

    @abstractmethod
    def handle_request(self, request_type, content):
        """
        Handle different types of requests.
        This method must be implemented in subclasses.
        """
        pass
