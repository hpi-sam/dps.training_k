import traceback
import json
from abc import ABC, abstractmethod

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from rest_framework.authtoken.models import Token

from game.models import PatientInstance, Exercise
from template.models import Action, Resource
from template.serializers import ResourceSerializer


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
        SUCCESS = "success"
        EXERCISE = "exercise"
        AVAILABLE_ACTIONS = "available-actions"
        AVAILABLE_MATERIAL = "available-material"

    class ClosureCodes:
        UNKNOWN = 0
        NOT_AUTHENTICATED = 401

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = ""
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
        patient, _ = PatientInstance.objects.get_or_create(
            name="Max Mustermann", exercise=self.exercise, patient_id=2
        )
        exercise_object = {
            "exercise": {
                "exerciseId": exercise.exerciseId,
                "areas": [
                    {
                        "areaName": "X",
                        "patients": [
                            {
                                "patientId": patient.patient_id,
                                "patientName": patient.name,
                                "patientCode": 0,
                                "triage": patient.triage,
                            }
                        ],
                        "personnel": [{"personnelId": 0, "personnelName": "X"}],
                        "material": [{"materialId": 0, "materialName": "X"}],
                    }
                ],
            }
        }
        self.send_event(self.OutgoingMessageTypes.EXERCISE, exercise=exercise_object)

    def send_available_actions(self):
        actions = Action.objects.all()
        actions = [
            {
                "actionName": action.name,
                "actionCategory": action.category,
            }
            for action in actions
        ]
        self.send_event(
            self.OutgoingMessageTypes.AVAILABLE_ACTIONS, availableActions=actions
        )

    def send_available_material(self):
        materials = Resource.objects.all()
        materials = [
            {
                "materialName": material.name,
                "materialCategory": material.category,
            }
            for material in materials
        ]
        self.send_event(
            self.OutgoingMessageTypes.AVAILABLE_MATERIAL, availableMaterial=materials
        )

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def material_change_event(self, event):
        self._send_exercise(self.exercise)

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Helper functions
    # ------------------------------------------------------------------------------------------------------------------------------------------------

    def related_materials_list(self, area):
        entries = area.inventory.entries.all()
        materials = []
        for entry in entries:
            for _ in range(entry.amount):
                materials.append(ResourceSerializer(entry.resource).to_json())
