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
from template.serializers.continuous_variable_serializer import (
    ContinuousVariableSerializer,
)
from template.serializers.state_serialize import StateSerializer
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import (
    ChannelNotifier,
    PersonnelDispatcher,
    MaterialInstanceDispatcher,
)
from ..serializers.patient_relocating_serializer import PatientRelocatingSerializer
from ..serializers.resource_assignment_serializer import AreaResourceSerializer


class PatientConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class PatientIncomingMessageTypes:
        ACTION_ADD = "action-add"
        ACTION_CANCEL = "action-cancel"
        ACTION_CHECK = "action-check"
        ACTION_CHECK_STOP = "action-check-stop"
        EXAMPLE = "example"
        MATERIAL_ASSIGN = "material-assign"
        MATERIAL_RELEASE = "material-release"
        PATIENT_MOVE = "patient-move"
        PERSONNEL_ASSIGN = "personnel-assign"
        PERSONNEL_RELEASE = "personnel-release"
        TRIAGE = "triage"

    class PatientOutgoingMessageTypes:
        ACTION_CHECK = "action-check"
        ACTION_CONFIRMATION = "action-confirmation"
        ACTION_DECLINATION = "action-declination"
        ACTION_LIST = "action-list"
        RESOURCE_ASSIGNMENTS = "resource-assignments"
        RESPONSE = "response"
        STATE = "state"
        CONTINUOUS_VARIABLE = "continuous-variable"
        PATIENT_BACK = "patient-back"
        PATIENT_RELOCATING = "patient-relocating"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_arguments = [
            lambda: PatientInstance.objects.get(frontend_id=self.patient_frontend_id)
        ]
        self.patient_frontend_id = ""
        self.currently_inspected_action = None
        self.continuous_variables_hashes = {}

        patient_request_map = {
            self.PatientIncomingMessageTypes.ACTION_ADD: (
                self.handle_action_add,
                "actionName",
            ),
            self.PatientIncomingMessageTypes.ACTION_CANCEL: (
                self.handle_action_cancel,
                "actionId",
            ),
            self.PatientIncomingMessageTypes.ACTION_CHECK: (
                self.handle_action_check,
                "actionName",
            ),
            self.PatientIncomingMessageTypes.ACTION_CHECK_STOP: (
                self.handle_action_check_stop,
            ),
            self.PatientIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exerciseId",
                "patientId",
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
            self.PatientIncomingMessageTypes.TRIAGE: (
                self.handle_triage,
                "triage",
            ),
        }
        self.REQUESTS_MAP.update(patient_request_map)

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
            self.state_change_event()
            if self.exercise.is_running():
                self.exercise_start_event()
                self.action_list_event()
                self.resource_assignment_event()

        else:
            self.close()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # These methods are not allowed to be called directly. If you want to call them from the backend, go via self.receive_json()
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_action_add(self, patient_instance, action_name):
        action_template = Action.objects.get(name=action_name)
        kwargs = {}
        needed_arguments = ActionInstance.needed_arguments_create(action_template)
        for argument in needed_arguments:
            if argument == "patient_instance":
                kwargs["patient_instance"] = patient_instance
            elif argument == "destination_area":
                kwargs["destination_area"] = patient_instance.area
            elif argument == "lab":
                kwargs["lab"] = self.exercise.lab
        action_instance = ActionInstance.create(action_template, **kwargs)
        application_succeded, message = action_instance.try_application()
        if not application_succeded:
            self._send_action_declination(action_name=action_name, message=message)

    def handle_action_cancel(self, _, action_id):
        action_instance = ActionInstance.objects.get(id=action_id)
        success, message = action_instance.try_cancelation()
        if not success:
            self.send_failure(message=message)

    def handle_action_check(self, _, action_name):
        self._start_inspecting_action(action_name)
        action_template = Action.objects.get(name=action_name)
        if action_template.location == Action.Location.LAB:
            action_check_message = LabActionCheckSerializer(
                action_template, self.exercise.lab, self.patient_instance
            ).data
        else:
            action_check_message = PatientInstanceActionCheckSerializer(
                action_template, self.patient_instance
            ).data
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CHECK,
            **action_check_message,
        )

    def handle_action_check_stop(self, _):
        self._stop_inspecting_action(self.currently_inspected_action)

    def handle_example(self, _, exercise_frontend_id, patient_frontend_id):
        self.exercise_frontend_id = exercise_frontend_id
        self.patient_frontend_id = patient_frontend_id
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id} & patientId {self.patient_frontend_id}",
        )

    def handle_material_assign(self, patient_instance, material_id):
        material_instance = MaterialInstance.objects.get(id=material_id)
        succeeded, message = material_instance.try_moving_to(patient_instance)
        if not succeeded:
            self.send_failure(message=message)

    def handle_material_release(self, patient_instance, material_id):
        material_instance = MaterialInstance.objects.get(id=material_id)
        area = patient_instance.area
        succeeded, message = material_instance.try_moving_to(area)
        if not succeeded:
            self.send_failure(message=message)

    def handle_patient_move(self, patient_instance, area_id):
        area = Area.objects.get(id=area_id)
        succeeded, message = patient_instance.try_moving_to(area)

        if not succeeded:
            self.send_failure(message=message)
            return

        if message is not None and message != "":
            self.send_warning(
                message=message,
            )

    def handle_personnel_assign(self, patient_instance, personnel_id):
        personnel = Personnel.objects.get(id=personnel_id)
        succeeded, message = personnel.try_moving_to(patient_instance)
        if not succeeded:
            self.send_failure(message=message)

    def handle_personnel_release(self, patient_instance, personnel_id):
        personnel = Personnel.objects.get(id=personnel_id)
        area = patient_instance.area
        succeeded, message = personnel.try_moving_to(area)
        if not succeeded:
            self.send_failure(message=message)

    def handle_triage(self, patient_instance, triage):
        patient_instance.triage = triage
        patient_instance.save(update_fields=["triage"])

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

    def state_change_event(self, event=None):
        serialized_state = StateSerializer(
            self.get_patient_instance().patient_state
        ).data
        self.send_event(
            self.PatientOutgoingMessageTypes.STATE,
            state=serialized_state,
        )

    def continuous_variable_event(self, event=None):
        serialized_continuous_state = ContinuousVariableSerializer(
            self.get_patient_instance()
        ).data

        continuous_variables = serialized_continuous_state["continuousVariables"]
        filtered_continuous_variables = [
            variable
            for variable in continuous_variables
            if self.has_continuous_variable_hash_changed(variable)
        ]
        self.update_continuous_variable_hashes(filtered_continuous_variables)
        serialized_continuous_state["continuousVariables"] = (
            filtered_continuous_variables
        )

        self.send_event(
            self.PatientOutgoingMessageTypes.CONTINUOUS_VARIABLE,
            continuousState=serialized_continuous_state,
        )

    def has_continuous_variable_hash_changed(self, variable):
        """Check if the hash of the variable has changed."""
        var_name = variable["name"]
        var_hash = variable["hash"]
        if var_name not in self.continuous_variables_hashes:
            return True
        return self.continuous_variables_hashes[var_name] != var_hash

    def update_continuous_variable_hashes(self, variables):
        """Update the stored hashes with the new hashes."""
        for variable in variables:
            self.continuous_variables_hashes[variable["name"]] = variable["hash"]

    def exercise_start_event(self, event=None):
        super().exercise_start_event(event)
        self.continuous_variable_event()

    def action_check_changed_event(self, event=None):
        if self.currently_inspected_action:
            self.receive_json(
                {
                    "messageType": self.PatientIncomingMessageTypes.ACTION_CHECK,
                    "actionName": self.currently_inspected_action,
                }
            )

    def action_confirmation_event(self, event):
        action_instance = ActionInstance.objects.get(id=event["action_instance_id"])
        self.send_event(
            self.PatientOutgoingMessageTypes.ACTION_CONFIRMATION,
            actionId=action_instance.id,
            actionName=action_instance.name,
        )

    def action_list_event(self, event=None):
        actions = []

        """all action_instances where either the patient_instance is self.patient_instance or 
        the category is production and the area is the same as the patient_instance.area"""
        action_instances = (
            ActionInstance.objects.filter(
                Q(patient_instance=self.get_patient_instance())
                | Q(
                    template__category=Action.Category.PRODUCTION,
                    destination_area=self.get_patient_instance().area,
                )
            )
            .exclude(current_state__name=ActionInstanceStateNames.ON_HOLD)
            .exclude(current_state__name=ActionInstanceStateNames.CANCELED)
        )
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

    def relocation_start_event(self, event):
        self.unsubscribe(ChannelNotifier.get_group_name(self.exercise))
        action_instance = ActionInstance.objects.get(id=event["action_instance_id"])
        self.send_event(
            self.PatientOutgoingMessageTypes.PATIENT_RELOCATING,
            **PatientRelocatingSerializer(action_instance).data,
        )

    def relocation_end_event(self, event=None):
        self.subscribe(ChannelNotifier.get_group_name(self.exercise))
        self.send_event(
            self.PatientOutgoingMessageTypes.PATIENT_BACK,
        )

    def send_exercise_event(self, event):
        if (
            not self.get_patient_instance().area
        ):  # frontend assumes that patients are always in an area
            return
        super().send_exercise_event(event)

    def resource_assignment_event(self, event=None):
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
