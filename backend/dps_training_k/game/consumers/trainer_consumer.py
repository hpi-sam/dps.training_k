from .abstract_consumer import AbstractConsumer
from game.models import Exercise


class TrainerConsumer(AbstractConsumer):
    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        CREATE_EXERCISE = "trainer-exercise-create"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-create"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = None
        self.REQUESTS_MAP = {
            self.TrainerIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
            ),
            self.TrainerIncomingMessageTypes.CREATE_EXERCISE: (
                self.handle_create_exercise,
            ),
        }

    def connect(self):
        self.accept()

    def handle_example(self, exercise_code):
        self.exercise_code = exercise_code
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code}",
        )

    def handle_create_exercise(self):
        try:
            exercise = Exercise()
        except Exception as e:
            print("an error has occured: ", str(e))

        exercise_object = {
            "exerciseCode": 123456,
            "areas": [
                {
                    "name": "ZNA",
                    "patients": [
                        {
                            "name": "Max Mustermann",
                            "patientCode": 123456,
                            "patientId": 5,
                            "patientDatabaseId": 3,
                        }
                    ],
                    "personnel": [
                        {
                            "name": "Hanna Schulz",
                            "role": "Arzt",
                            "personnelDatabaseId": 6,
                        }
                    ],
                    "devices": [{"name": "EKG", "deviceDatabaseId": 15}],
                }
            ],
        }
        self.send_event(
            self.TrainerOutgoingMessageTypes.EXERCISE_CREATED, exercise=exercise_object
        )
