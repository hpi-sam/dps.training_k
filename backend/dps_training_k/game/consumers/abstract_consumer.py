import traceback

from asgiref.sync import async_to_sync
from abc import ABC, abstractmethod
from channels.generic.websocket import JsonWebsocketConsumer


class AbstractConsumer(JsonWebsocketConsumer, ABC):
    """
    Base consumer to be used as an abstract class, preparing some shared behaviour, but never to
    be used directly.
    """

    class OutgoingMessageTypes:
        FAILURE = "failure"
        SUCCESS = "success"

    class FailureCodes:
        UNKNOWN = 0
        INCORRECT_REQUEST_TYPE = 1
        MISSING_KEYS = 2
        INCORRECT_KEY_FORMAT = 3
        DATABASE_NOT_FOUND = 4
        MISSING_REQUEST_TYPE = 5
        INVALID_INTERNAL_MESSAGE = 6

    class ClosureCodes:
        UNKNOWN = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = ""
        self.REQUESTS_MAP = {}

    @abstractmethod
    def connect(self):
        pass

    def disconnect(self, close_code):
        pass  # Add any cleanup here

    def send_event(self, event_type, content=None, **kwargs):
        """
        Wrapper to send_json() in order to have always the same structure: at least a type and often a content.
        Allows some other high level information in the kwargs.
        """
        d = {"type": event_type}
        if content:
            d["content"] = content
        for key, value in kwargs.items():
            d[key] = value
        self.send_json(d)

    def send_failure(self, message="unknown failure", code=0, **kwargs):
        message_dict = {
            "type": self.OutgoingMessageTypes.FAILURE,
            "message": message,
            "code": code,
        }
        for key, value in kwargs.items():
            message_dict[key] = value
        self.send_json(message_dict)

    def send_validation(self, request_type, **kwargs):
        """
        Wrapper to send_json() in order to always have the same structure. Notifies the client
        that the asked request was evaluated and executed.
        """
        d = {"type": self.OutgoingMessageTypes.SUCCESS, "request": request_type}
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
        request_type = content.get("type")

        if not request_type:
            self.send_failure(
                "Incoming message is without request type.",
                code=self.FailureCodes.MISSING_REQUEST_TYPE,
            )
            return

        try:
            method, *keys = self.REQUESTS_MAP[request_type]
        except KeyError:
            self.send_failure(
                f"Invalid request type '{request_type}' for incoming message.",
                code=self.FailureCodes.INCORRECT_REQUEST_TYPE,
            )
            return

        complete = True
        args = []
        for key in keys:
            if key not in content:
                self.send_failure(
                    f'Key "{key}" is missing for this request type',
                    code=self.FailureCodes.MISSING_KEYS,
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
