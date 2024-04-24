from urllib.parse import parse_qs

from game.models import (
    PatientInstance,
    Exercise,
    ActionInstance,
)
from template.models import Action
from template.serializer.state_serialize import StateSerializer
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier


class PatientConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
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
        STATE_CHANGE = "state-change"
        ACTION_CONFIRMATION = "action-confirmation"
        ACTION_DECLINATION = "action-declination"
        ACTION_RESULT = "action-result"
        ACTION_CHECK = "action-check"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_patient_frontend_id = ""
        self.REQUESTS_MAP = {
            self.PatientIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exerciseId",
                "patientId",
            ),
            self.PatientIncomingMessageTypes.TEST_PASSTHROUGH: (
                self.handle_test_passthrough,
            ),
            self.PatientIncomingMessageTypes.TRIAGE: (
                self.handle_triage,
                "triage",
            ),
            self.PatientIncomingMessageTypes.ACTION_ADD: (
                self.handle_action_add,
                "action_id",
            ),
        }

    @property
    def patient_instance(self):
        if not self.patient_frontend_id:
            return None
        return PatientInstance.objects.get(
            patient_frontend_id=self.patient_frontend_id
        )  # This enforces patient_instance to always work with valid data

    def connect(self):
        # example trainer creation for testing purposes as long as the actual exercise flow is not useful for patient route debugging
        self.tempExercise = Exercise.createExercise()
        # example patient creation for testing purposes as long as the actual patient flow is not implemented
        from template.tests.factories.patient_state_factory import PatientStateFactory

        self.temp_state = PatientStateFactory(10, 2)
        PatientInstance.objects.create(
            name="Max Mustermann",
            exercise=self.exercise,
            patient_frontend_id=2,  # has to be the same as the username in views.py#post
            exercise_id=self.tempExercise.id,
            patient_state=self.temp_state,
        )

        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, patient_frontend_id = self.authenticate(token)
        if success:
            self.patient_frontend_id = patient_frontend_id

            self.exercise = self.patient_instance.exercise
            self.accept()
            self.subscribe(ChannelNotifier.get_group_name(self.patient_instance))
            self.subscribe(ChannelNotifier.get_group_name(self.exercise))
            self._send_exercise(exercise=self.exercise)
            self.send_available_actions()
            self.send_available_patients()

    def disconnect(self, code):
        # example patient_instance deletion - see #connect
        self.patient_instance.delete()
        # example trainer deletion - see #connect
        self.tempExercise.delete()
        self.temp_state.delete()
        super().disconnect(code)

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_example(self, exercise_frontend_id, patient_frontend_id):
        self.exercise_frontend_id = exercise_frontend_id
        self.patient_frontend_id = patient_frontend_id
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id} & patientId {self.patient_frontend_id}",
        )

    def handle_test_passthrough(self):
        self.send_event(
            self.PatientOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_triage(self, triage):
        patient_instance = self.patient_instance
        patient_instance.triage = triage
        patient_instance.save(update_fields=["triage"])

    def handle_action_add(self, action_id):
        action = Action.objects.get(pk=action_id)
        action_instance = ActionInstance.create(self.patient_instance, action)
        action_instance.try_application()

    def handle_action_check(self, action_id):
        stub_action_name = "Recovery Position"
        stub_time = 10
        stub_requirements = [
            {
                "name": "a recovery position condition",
                "category": "material",
                "values": [{"available": 1, "assigned": 1, "needed": 1}],
            }
        ]
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CHECK,
            actionName=stub_action_name,
            time=stub_time,
            requirements=stub_requirements,
        )

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def state_change_event(self, event):
        serialized_state = StateSerializer(self.patient_instance.state).data
        self.send_event(
            self.PatientOutgoingMessageTypes.STATE_CHANGE,
            **serialized_state,
        )

    def action_confirmation_event(self, event):
        action_instance = ActionInstance.objects.get(pk=event["action_instance_pk"])
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CONFIRMATION,
            actionId=action_instance.id,
            actionName=action_instance.name,
        )

    def action_declination_event(self, event):
        action_instance = ActionInstance.objects.get(pk=event["action_instance_pk"])
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_DECLINATION,
            actionName=action_instance.name,
            actionDeclinationReason=action_instance.current_state.info_text,
        )

    def action_result_event(self, event):
        action_instance = ActionInstance.objects.get(pk=event["action_instance_pk"])
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_RESULT,
            actionId=action_instance.id,
            actionResult=action_instance.result,
        )
