import traceback
from abc import ABC, abstractmethod

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token

from game.models import Exercise
from game.serializers.exercise_serializer import ExerciseSerializer
from template.models import Action, PatientInformation, Material
from template.serializers import (
    MaterialSerializer,
    PatientInformationSerializer,
    ActionSerializer,
)


class AbstractConsumer(JsonWebsocketConsumer, ABC):
    """
    Base consumer to be used as an abstract class, preparing some shared behaviour, but never to
    be used directly.
    Inheriting classes are responsible for DECODING messages from the frontend into method calls and
    ENCODING events from the backend into JSONs to send to the frontend. When encoding events this also implies
    deciding what part of the event should be sent to the frontend(filtering).
    """

    class OutgoingMessageTypes:
        FAILURE = "failure"
        WARNING = "warning"
        SUCCESS = "success"
        EXERCISE = "exercise"
        EXERCISE_START = "exercise-start"
        EXERCISE_END = "exercise-end"
        EXERCISE_PAUSE = "exercise-pause"
        EXERCISE_RESUME = "exercise-resume"
        AVAILABLE_ACTIONS = "available-actions"
        AVAILABLE_PATIENTS = "available-patients"
        AVAILABLE_MATERIALS = "available-materials"

    class ClosureCodes:
        UNKNOWN = 0
        NOT_AUTHENTICATED = 401

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_frontend_id = ""
        self.exercise = None
        self.REQUESTS_MAP = {}
        self.user = None

    @abstractmethod
    def connect(self):
        pass

    def send_event(self, event_type, **kwargs):
        """
        Wrapper to send_json() in order to always have the same structure: at least a messageType and often content.
        Allows some other high level information in the kwargs.
        """
        d = {"messageType": event_type}
        for key, value in kwargs.items():
            d[key] = value
        self.send_json(d)

    def send_failure(self, message="unknown failure", **kwargs):
        message_dict = {
            "messageType": self.OutgoingMessageTypes.FAILURE,
            "message": message,
        }
        for key, value in kwargs.items():
            message_dict[key] = value
        self.send_json(message_dict)

    def send_warning(self, message="unknown warning", **kwargs):
        message_dict = {
            "messageType": self.OutgoingMessageTypes.WARNING,
            "message": message,
        }
        for key, value in kwargs.items():
            message_dict[key] = value
        self.send_json(message_dict)

    def send_validation(self, request_type, **kwargs):
        """
        Wrapper to send_json() in order to always have the same structure. Notifies the client
        that the asked request was evaluated and executed.
        """
        d = {"messageType": self.OutgoingMessageTypes.SUCCESS, "request": request_type}
        for key, value in kwargs.items():
            d[key] = value
        self.send_json(d)

    # entry point function for all incoming WebSocket messages
    def receive_json(self, content):
        self.dispatch_request(content)

    def dispatch_request(self, content):
        """
        Util method to call a specific method based on the request type and verify that the required parameters exist in the given dictionary
        content.
        If the given type is not valid, sends a failure message with code INCORRECT_REQUEST_TYPE.
        If all parameters for the method are in content, calls the method with these params. Else it sends a failure
        message with code MISSING_KEYS for each missing key.
        :param content: A dictionary that should contain 'type' and all required params for the method corresponding
        to this type
        """
        request_type = content.get("messageType")

        if not request_type:
            self.send_failure(
                "Incoming message is without request type.",
            )
            return

        try:
            method, *keys = self.REQUESTS_MAP[request_type]
        except KeyError:
            self.send_failure(
                f"Invalid request type '{request_type}' for incoming message.",
            )
            return

        complete = True
        args = []
        # add default arguments for inheriting consumers based on a lambda function supplied by them
        for argument in self.default_arguments:
            args.append(argument())
        for key in keys:
            if key not in content:
                self.send_failure(
                    f'Key "{key}" is missing for this request type',
                )
                complete = False
            else:
                args.append(content[key])
        if complete:
            try:
                method(*args)
            except Exception as e:
                print(traceback.format_exc())
                self.send_failure(message=str(e))

    def subscribe(self, group_name):
        async_to_sync(self.channel_layer.group_add)(
            group_name,
            self.channel_name,
        )

    def unsubscribe(self, group_name):
        async_to_sync(self.channel_layer.group_discard)(
            group_name,
            self.channel_name,
        )

    def group_send(self, group_name, event):
        async_to_sync(self.channel_layer.group_send)(group_name, event)

    def disconnect(self, code):
        # if self.user:
        #     self.user.clear_channel_name()
        code = self.ClosureCodes.UNKNOWN if not code else code
        super().disconnect(code)

    def authenticate(self, token):
        try:
            token = Token.objects.get(key=token)
            self.user = token.user
            self.user.set_channel_name(self.channel_name)
            return True, self.user.username
        except Token.DoesNotExist:
            self.close(code=self.ClosureCodes.NOT_AUTHENTICATED)
            return False, None

    def send_exercise_event(self, event):
        exercise = Exercise.objects.get(pk=event["exercise_pk"])
        self._send_exercise(exercise=exercise)

    def _send_exercise(self, exercise):
        self.send_event(
            self.OutgoingMessageTypes.EXERCISE,
            exercise=ExerciseSerializer(exercise).data,
        )

    def send_available_actions(self):
        actions = Action.objects.all()
        actions = [ActionSerializer(action).data for action in actions]
        self.send_event(
            self.OutgoingMessageTypes.AVAILABLE_ACTIONS, availableActions=actions
        )

    def send_available_patients(self):
        patientsInformation = PatientInformation.objects.all()
        availablePatients = [
            PatientInformationSerializer(patient_information).data
            for patient_information in patientsInformation
        ]
        self.send_event(
            self.OutgoingMessageTypes.AVAILABLE_PATIENTS,
            availablePatients=availablePatients,
        )

    def send_available_materials(self):
        materials = Material.objects.all()
        availableMaterials = [
            MaterialSerializer(material).data for material in materials
        ]
        self.send_event(
            self.OutgoingMessageTypes.AVAILABLE_MATERIALS,
            availableMaterials=availableMaterials,
        )

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def exercise_start_event(self, event=None):
        self.send_event(self.OutgoingMessageTypes.EXERCISE_START)

    def exercise_end_event(self, event=None):
        self.send_event(self.OutgoingMessageTypes.EXERCISE_END)
        self.close()

    def exercise_resume_event(self, event):
        raise NotImplementedError(
            """Introducing resuming feature requires reworking the dispatch method inside ExerciseDispatcher. 
            It currently sends "exercise-start" every time it enters the running state"""
        )

    def resource_assignment_event(self, event):
        """Needs to be implemented here to send this event on_exercise_start via channel_notifications to patient_consumer"""
        pass

    def imaging_action_start_event(self, event):
        """Needs to be implemented here to send this event on_exercise_start via channel_notifications to patient_consumer"""
        pass

    def imaging_action_end_event(self, event):
        """Needs to be implemented here to send this event on_exercise_start via channel_notifications to patient_consumer"""
        pass
