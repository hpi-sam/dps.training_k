from urllib.parse import parse_qs

from game.models import (
    PatientInstance,
    MaterialInstance,
    ActionInstance,
    ScheduledEvent,
)
from template.models import Action
from template.serializers.state_serialize import StateSerializer
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
        MATERIAL_RELEASE = "material-release"
        MATERIAL_ASSIGN = "material-assign"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"
        TEST_PASSTHROUGH = "test-passthrough"
        STATE_CHANGE = "state-change"
        ACTION_CONFIRMATION = "action-confirmation"
        ACTION_DECLINATION = "action-declination"
        ACTION_LIST = "action-list"
        ACTION_CHECK = "action-check"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_frontend_id = ""
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
                "actionName",
            ),
            self.PatientIncomingMessageTypes.MATERIAL_RELEASE: (
                self.handle_material_release,
                "material_id",
            ),
            self.PatientIncomingMessageTypes.MATERIAL_ASSIGN: (
                self.handle_material_assign,
                "material_id",
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
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, patient_frontend_id = self.authenticate(token)
        if success:
            self.patient_frontend_id = patient_frontend_id

            self.exercise = self.patient_instance.exercise
            self.accept()
            self.subscribe(ChannelNotifier.get_group_name(self.patient_instance))
            self.subscribe(ChannelNotifier.get_group_name(self.exercise))
            self.subscribe(ChannelNotifier.get_group_name(self.patient_instance.area))
            self.subscribe(ChannelNotifier.get_group_name(self.exercise.lab))
            self._send_exercise(exercise=self.exercise)
            self.send_available_actions()
            self.send_available_patients()
            self.action_list_event(None)

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
        self.patient_instance.triage = triage
        self.patient_instance.save(update_fields=["triage"])

    def handle_action_add(self, action_name):
        try:
            action_template = Action.objects.get(name=action_name)
            if action_template.category is Action.Category.PRODUCTION:
                action_instance = ActionInstance.create(
                    action_template,
                    lab=self.exercise.lab,
                    area=self.patient_instance.area,
                )
            else:
                action_instance = ActionInstance.create(
                    action_template=action_template,
                    patient_instance=self.patient_instance,
                )
            action_instance.try_application()
        except:
            self._send_action_declination(action_instance=action_instance)

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

    def handle_material_release(self, material_id):
        material_instance = MaterialInstance.objects.get(pk=material_id)
        area = self.patient_instance.area
        succeeded = material_instance.try_moving_to(area)
        if not succeeded:
            self.send_failure(
                message="Dieses Material wird aktuell verwendet. Es kann nicht verschoben werden."
            )

    def handle_material_assign(self, material_id):
        material_instance = MaterialInstance.objects.get(pk=material_id)
        succeeded = material_instance.try_moving_to(self.patient_instance)
        if not succeeded:
            self.send_failure(
                message="Dieses Material wird aktuell verwendet. Es kann nicht verschoben werden."
            )

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # methods used internally
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def _send_action_declination(self, action_instance):
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_DECLINATION,
            actionName=action_instance.name,
            actionDeclinationReason=action_instance.current_state.info_text,
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

    def action_list_event(self, event):
        actions = []
        for action_instance in ActionInstance.objects.filter(
            patient_instance=self.patient_instance
        ):
            action_data = {
                "actionId": action_instance.id,
                "orderId": action_instance.order_id,
                "actionName": action_instance.name,
                "actionStatus": action_instance.state_name,
                "timeUntilCompletion": (
                    ScheduledEvent.get_time_until_completion(action_instance)
                    if not action_instance.completed
                    else None
                ),
                "actionResult": action_instance.result,
            }

            actions.append(action_data)
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_LIST,
            actions=actions,
        )
