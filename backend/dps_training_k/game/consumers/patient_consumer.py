from .abstract_consumer import AbstractConsumer


class PatientConsumer(AbstractConsumer):#
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_code = ""

    def connect(self):
        self.exercise_code = self.scope["url_route"]["kwargs"]["exercise_code"]
        self.patient_code = self.scope["url_route"]["kwargs"]["patient_code"]
        self.accept()

    def handle_request(self, request_type, content):
        # Implementation for handling requests
        if request_type == "example":
            self.handle_example(content)
        else:
            self.send_json({"error": "Unknown request type"})

    def handle_example(self, content):
        # Process the 'example' request type
        response = {"type": "response", "content": f"exercise_code {self.exercise_code} & patient_code {self.patient_code}"}
        self.send_json(response)

    # You can add more methods specific to MyConsumer here
