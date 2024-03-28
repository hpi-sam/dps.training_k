from .abstract_consumer import AbstractConsumer
from urllib.parse import parse_qs
from game.models import Patient


class PatientConsumer(AbstractConsumer):
    class PatientIncomingMessageTypes:
        EXAMPLE = "example"
        TEST_PASSTHROUGH = "test-passthrough"
        TRIAGE = "triage"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"
        TEST_PASSTHROUGH = "test-passthrough"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patientId = ""
        self.patient = None
        self.REQUESTS_MAP = {
            self.PatientIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
                "patient_code",
            ),
            self.PatientIncomingMessageTypes.TEST_PASSTHROUGH: (
                self.handle_test_passthrough,
            ),
            self.PatientIncomingMessageTypes.TRIAGE: (
                self.handle_triage,
                "triage",
            ),
        }

    def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, patientId = self.authenticate(token)
        if success:
            self.patient = Patient.objects.get(patientId=patientId)
            self.patientId = patientId
            self.exercise = self.patient.exercise
            self.accept()
            self._send_exercise()

    def handle_example(self, exercise_code, patient_code):
        self.exercise_code = exercise_code
        self.patientId = patient_code
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code} & patient_code {self.patientId}",
        )

    def handle_test_passthrough(self):
        self.send_event(
            self.PatientOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )
    
    def handle_triage(self, triage):
        self.patient.triage = triage
        self._send_exercise()
