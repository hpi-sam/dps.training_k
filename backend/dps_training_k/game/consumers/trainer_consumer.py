from .abstract_consumer import AbstractConsumer


class TrainerConsumer(AbstractConsumer):
    def connect(self):
        self.exercise_code = self.scope["url_route"]["kwargs"]["exercise_code"]
        self.accept()

    def handle_request(self, request_type, content):
        # Implementation for handling requests
        if request_type == "example":
            self.handle_example(content)
        else:
            self.send_json({"error": "Unknown request type"})

    def handle_example(self, content):
        # Process the 'example' request type
        response = {"type": "response", "content": "Example processed"}
        self.send_json(response)
