from .abstract_consumer import AbstractConsumer
from urllib.parse import parse_qs
from game.models import Exercise, Patient


class PatientConsumer(AbstractConsumer):
    class PatientIncomingMessageTypes:
        EXAMPLE = "example"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_code = ""
        self.REQUESTS_MAP = {
            self.PatientIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
                "patient_code",
            )
        }

    def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        if self.authenticate(token):
            self.accept()
            self._send_exercise()

    def handle_example(self, exercise_code, patient_code):
        self.exercise_code = exercise_code
        self.patient_code = patient_code
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code} & patient_code {self.patient_code}",
        )
