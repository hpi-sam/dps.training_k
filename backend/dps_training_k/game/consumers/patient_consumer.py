from .abstract_consumer import AbstractConsumer


class PatientConsumer(AbstractConsumer):
    class PatientIncomingMessageTypes:
        EXAMPLE = "example"

    class PatientOutgoingMessageTypes:
        RESPONSE = "response"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_code = ""
        self.REQUESTS_MAP = {
            self.PatientIncomingMessageTypes.EXAMPLE: (self.handle_example,)
        }

    def connect(self):
        self.exercise_code = self.scope["url_route"]["kwargs"]["exercise_code"]
        self.patient_code = self.scope["url_route"]["kwargs"]["patient_code"]
        self.accept()

    def handle_example(self):
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            f"exercise_code {self.exercise_code} & patient_code {self.patient_code}",
        )
