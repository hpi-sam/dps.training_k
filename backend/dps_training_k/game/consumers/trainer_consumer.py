from .abstract_consumer import AbstractConsumer


class TrainerConsumer(AbstractConsumer):
    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.REQUESTS_MAP = {
            self.TrainerIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
            )
        }

    def connect(self):
        self.accept()

    def handle_example(self, exercise_code):
        self.exercise_code = exercise_code
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            f"exercise_code {self.exercise_code}",
        )
