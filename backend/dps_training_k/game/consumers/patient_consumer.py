from urllib.parse import parse_qs

from django.db.models import Q

from game.models import (
    PatientInstance,
    MaterialInstance,
    ActionInstance,
    ScheduledEvent,
    Personnel,
    ActionInstanceStateNames,
    Area,
)
from game.serializers.action_check_serializers import (
    PatientInstanceActionCheckSerializer,
    LabActionCheckSerializer,
)
from template.models import Action
from template.serializers.state_serialize import StateSerializer
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import (
    ChannelNotifier,
    PersonnelDispatcher,
    MaterialInstanceDispatcher,
)
from ..serializers.resource_assignment_serializer import AreaResourceSerializer


class PatientConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class PatientIncomingMessageTypes:
        EXAMPLE = "example"
        TEST_PASSTHROUGH = "test-passthrough"
        TRIAGE = "triage"
        ACTION_CHECK = "action-check"
        ACTION_CHECK_STOP = "action-check-stop"
        ACTION_ADD = "action-add"
        MATERIAL_ASSIGN = "material-assign"
        MATERIAL_RELEASE = "material-release"
        PATIENT_MOVE = "patient-move"
        PERSONNEL_ASSIGN = "personnel-assign"
        PERSONNEL_RELEASE = "personnel-release"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE = "exercise"
        TEST_PASSTHROUGH = "test-passthrough"
        ACTION_CONFIRMATION = "action-confirmation"
        ACTION_DECLINATION = "action-declination"
        ACTION_LIST = "action-list"
        ACTION_CHECK = "action-check"
        RESOURCE_ASSIGNMENTS = "resource-assignments"
        STATE_CHANGE = "state"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_arguments = [
            lambda: PatientInstance.objects.get(frontend_id=self.patient_frontend_id)
        ]
        self.patient_frontend_id = ""
        self.currently_inspected_action = None
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
            self.PatientIncomingMessageTypes.ACTION_CHECK: (
                self.handle_action_check,
                "actionName",
            ),
            self.PatientIncomingMessageTypes.ACTION_CHECK_STOP: (
                self.handle_action_check_stop,
            ),
            self.PatientIncomingMessageTypes.ACTION_ADD: (
                self.handle_action_add,
                "actionName",
            ),
            self.PatientIncomingMessageTypes.MATERIAL_ASSIGN: (
                self.handle_material_assign,
                "materialId",
            ),
            self.PatientIncomingMessageTypes.MATERIAL_RELEASE: (
                self.handle_material_release,
                "materialId",
            ),
            self.PatientIncomingMessageTypes.PATIENT_MOVE: (
                self.handle_patient_move,
                "areaId",
            ),
            self.PatientIncomingMessageTypes.PERSONNEL_ASSIGN: (
                self.handle_personnel_assign,
                "personnelId",
            ),
            self.PatientIncomingMessageTypes.PERSONNEL_RELEASE: (
                self.handle_personnel_release,
                "personnelId",
            ),
        }

    def get_patient_instance(self):
        # this enforces that we always work with up to date data from the database
        # if you want to update values, copy the instance this function returns and work with that.
        self.patient_instance.refresh_from_db()
        return self.patient_instance

    def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, patient_frontend_id = self.authenticate(token)
        if success:
            self.patient_frontend_id = patient_frontend_id
            self.patient_instance = PatientInstance.objects.get(
                frontend_id=self.patient_frontend_id
            )

            self.exercise = self.patient_instance.exercise
            self.accept()
            self.subscribe(ChannelNotifier.get_group_name(self.patient_instance))
            self.subscribe(ChannelNotifier.get_group_name(self.exercise))
            self.subscribe(ChannelNotifier.get_group_name(self.patient_instance.area))
            self.subscribe(ChannelNotifier.get_group_name(self.exercise.lab))
            self._send_exercise(exercise=self.exercise)
            self.send_available_actions()
            self.send_available_patients()
            self.state_change_event(None)
            if self.exercise.is_running():
                self.exercise_start_event(None)
                self.action_list_event(None)
                self.resource_assignment_event(None)

        else:
            self.close()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # These methods are not allowed to be called directly. If you want to call them from the backend, go via self.receive_json()
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_example(
        self, patient_instance, exercise_frontend_id, patient_frontend_id
    ):
        self.exercise_frontend_id = exercise_frontend_id
        self.patient_frontend_id = patient_frontend_id
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id} & patientId {self.patient_frontend_id}",
        )

    def handle_test_passthrough(self, patient_instance):
        self.send_event(
            self.PatientOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_triage(self, patient_instance, triage):
        patient_instance.triage = triage
        patient_instance.save(update_fields=["triage"])

    def handle_action_add(self, patient_instance, action_name):
        action_template = Action.objects.get(name=action_name)
        if action_template.category == Action.Category.PRODUCTION:
            action_instance = ActionInstance.create(
                template=action_template,
                lab=self.exercise.lab,
                area=patient_instance.area,
            )
        else:
            action_instance = ActionInstance.create(
                template=action_template,
                patient_instance=patient_instance,
            )
        application_succeded, context = action_instance.try_application()
        if not application_succeded:
            self._send_action_declination(action_name=action_name, message=context)

    def handle_action_check(self, patient_instance, action_name):
        self._start_inspecting_action(action_name)
        action_template = Action.objects.get(name=action_name)
        if action_template.category == Action.Category.PRODUCTION:
            action_check_message = LabActionCheckSerializer(
                action_template, self.exercise.lab
            ).data
        else:
            action_check_message = PatientInstanceActionCheckSerializer(
                action_template, self.patient_instance
            ).data
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CHECK,
            **action_check_message,
        )

    def handle_action_check_stop(self, patient_instance):
        self._stop_inspecting_action(self.currently_inspected_action)

    def handle_material_release(self, patient_instance, material_id):
        material_instance = MaterialInstance.objects.get(pk=material_id)
        area = patient_instance.area
        succeeded, msg = material_instance.try_moving_to(area)
        if not succeeded:
            self.send_failure(message=msg)

    def handle_material_assign(self, patient_instance, material_id):
        material_instance = MaterialInstance.objects.get(pk=material_id)
        succeeded, msg = material_instance.try_moving_to(patient_instance)
        if not succeeded:
            self.send_failure(message=msg)

    def handle_patient_move(self, patient_instance, area_id):
        area = Area.objects.get(pk=area_id)
        succeeded, msg = patient_instance.try_moving_to(area)

        if not succeeded:
            self.send_failure(message=msg)
            return

        self.resource_assignment_event(None)
        if msg is not None and msg != "":
            self.send_warning(
                message=msg,
            )

    def handle_personnel_release(self, patient_instance, personnel_id):
        personnel = Personnel.objects.get(pk=personnel_id)
        area = patient_instance.area
        succeeded, msg = personnel.try_moving_to(area)
        if not succeeded:
            self.send_failure(message=msg)

    def handle_personnel_assign(self, patient_instance, personnel_id):
        personnel = Personnel.objects.get(pk=personnel_id)
        succeeded, msg = personnel.try_moving_to(patient_instance)
        if not succeeded:
            self.send_failure(message=msg)

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # methods used internally
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def _send_action_declination(self, action_name, message=None):
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_DECLINATION,
            actionName=action_name,
            actionDeclinationReason=(
                "Irgendetwas ist schiefgegangen" if not message else message
            ),
        )

    def _start_inspecting_action(self, action_name):
        if self.currently_inspected_action == action_name:
            return
        self.currently_inspected_action = action_name
        self.subscribe(PersonnelDispatcher.get_live_group_name(self.exercise))
        self.subscribe(MaterialInstanceDispatcher.get_live_group_name(self.exercise))

    def _stop_inspecting_action(self, action_name):
        if not self.currently_inspected_action == action_name:
            return
        self.currently_inspected_action = None
        self.unsubscribe(PersonnelDispatcher.get_live_group_name(self.exercise))
        self.unsubscribe(MaterialInstanceDispatcher.get_live_group_name(self.exercise))

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def state_change_event(self, event):
        serialized_state = StateSerializer(
            self.get_patient_instance().patient_state
        ).data
        self.send_event(
            self.PatientOutgoingMessageTypes.STATE_CHANGE,
            state=serialized_state,
        )

    def action_check_changed_event(self, event):
        if self.currently_inspected_action:
            self.receive_json(
                {
                    "messageType": self.PatientIncomingMessageTypes.ACTION_CHECK,
                    "actionName": self.currently_inspected_action,
                }
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

        """all action_instances where either the patient_instance is self.patient_instance or 
        the category is production and the area is the same as the patient_instance.area"""
        action_instances = ActionInstance.objects.filter(
            Q(patient_instance=self.get_patient_instance())
            | Q(
                template__category=Action.Category.PRODUCTION,
                area=self.get_patient_instance().area,
            )
        ).exclude(current_state__name=ActionInstanceStateNames.ON_HOLD)
        # ToDo: remove the filter for ON_HOLD actions, when the scheduler is implemented so that the actions are not forever stuck in ON_HOLD

        for action_instance in action_instances:
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

    def resource_assignment_event(self, event):
        patient_instance = self.get_patient_instance()

        if not patient_instance:
            return

        area = patient_instance.area

        if not area:
            self.send_event(
                self.PatientOutgoingMessageTypes.RESOURCE_ASSIGNMENTS,
                resourceAssignments=[],
            )

        area_data = AreaResourceSerializer(area).data
        self.send_event(
            self.PatientOutgoingMessageTypes.RESOURCE_ASSIGNMENTS,
            resourceAssignments=[area_data],
        )
