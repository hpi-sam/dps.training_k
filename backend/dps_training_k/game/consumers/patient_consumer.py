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
            self.PatientIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
                "patient_code",
            )
        }

    def connect(self):
        self.accept()

    def handle_example(self, exercise_code, patient_code):
        self.exercise_code = exercise_code
        self.patient_code = patient_code
        self.send_event(
            self.PatientOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code} & patient_code {self.patient_code}",
        )
