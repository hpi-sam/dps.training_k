from .abstract_consumer import AbstractConsumer
from urllib.parse import parse_qs
from game.models import Patient
from game import channel_notifications


class PatientConsumer(AbstractConsumer):
    """
    This class is responsible for DECODING messages from the frontend(user==patient) into method calls and
    ENCODING events from the backend into JSONs to send to the frontend. When encoding events this also implies
    deciding what part of the event should be sent to the frontend(filtering).
    """

    class PatientIncomingMessageTypes:
        EXAMPLE = "example"
        TEST_PASSTHROUGH = "test-passthrough"
        TRIAGE = "triage"
        ACTION_ADD = "action-add"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"
        TEST_PASSTHROUGH = "test-passthrough"
        ACTION_CONFIRMATION = "action-confirmation"
        ACTION_DECLINATION = "action-declination"
        ACTION_RESULT = "action-result"

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
            self.PatientIncomingMessageTypes.ACTION_ADD: (self.handle_action_add,),
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

    def action_confirmation_event(self, event):
        action = channel_notifications.get_applied_action_instance(event)
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CONFIRMATION,
            {"actionName": action.name, "actionId": action.id},
        )

    def action_declination_event(self, event):
        action = channel_notifications.get_applied_action_instance(event)
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_DECLINATION,
            {
                "actionName": action.name,
                "actionDeclinationReason": action.reason_of_declination,
            },
        )

    def action_result_event(self, event):
        action = channel_notifications.get_applied_action_instance(event)
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_RESULT,
            {
                "actionId": action.name,
                "actionResult": action.result,
            },
        )
