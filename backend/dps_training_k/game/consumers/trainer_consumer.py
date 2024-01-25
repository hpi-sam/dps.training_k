from .abstract_consumer import AbstractConsumer


class TrainerConsumer(AbstractConsumer):
    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.REQUESTS_MAP = {
            self.TrainerIncomingMessageTypes.EXAMPLE: (self.handle_example,)
        }

    def connect(self):
        self.exercise_code = self.scope["url_route"]["kwargs"]["exercise_code"]
        self.accept()

    def handle_example(self):
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            f"exercise_code {self.exercise_code}",
        )
