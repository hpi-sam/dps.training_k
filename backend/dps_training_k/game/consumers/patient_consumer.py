from urllib.parse import parse_qs

from game.models import Patient, Exercise
from .abstract_consumer import AbstractConsumer
from template.serializer.state_serialize import StateSerializer


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

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"
        TEST_PASSTHROUGH = "test-passthrough"
        STATE_CHANGE = "state-change"

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
        # example trainer creation for testing purposes as long as the actual exercise flow is not useful for patient route debugging
        self.tempExercise = Exercise.createExercise()
        # example patient creation for testing purposes as long as the actual patient flow is not implemented
        from template.tests.factories.patient_state_factory import PatientStateFactory

        self.temp_state = PatientStateFactory(10, 2)
        Patient.objects.create(
            name="Max Mustermann",
            exercise=self.exercise,
            patientId=6,  # has to be the same as the username in views.py#post
            exercise_id=self.tempExercise.id,
            patient_state=self.temp_state,
        )

        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, patientId = self.authenticate(token)
        if success:
            self.patient = Patient.objects.get(patientId=patientId)
            self.patientId = patientId
            self.exercise = self.patient.exercise
            self.accept()
            self._send_exercise(exercise=self.exercise)

    def disconnect(self, code):
        # example patient deletion - see #connect
        self.patient.delete()
        # example trainer deletion - see #connect
        self.tempExercise.delete()
        self.temp_state.delete()
        super().disconnect(code)

    def handle_example(self, exercise_code, patient_code):
        self.exercise_code = exercise_code
        self.patientId = patient_code
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code} & patient_code {self.patientId}",
        )

    # comment
    def handle_test_passthrough(self):
        self.send_event(
            self.PatientOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_triage(self, triage):
        self.patient.triage = triage
        self._send_exercise(exercise=self.exercise)

    def state_change_event(self, event):
        serialized_state = StateSerializer(self.patient.state).data
        self.send_event(
            self.PatientOutgoingMessageTypes.STATE_CHANGE,
            **serialized_state,
        )
