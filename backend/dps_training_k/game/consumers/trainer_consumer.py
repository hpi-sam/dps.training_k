from .abstract_consumer import AbstractConsumer
from game.models import Exercise, Patient


class TrainerConsumer(AbstractConsumer):
    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        CREATE_EXERCISE = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"

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
            self.TrainerIncomingMessageTypes.TEST_PASSTHROUGH: (
                self.handle_test_passthrough,
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
        exercise = Exercise.createExercise()
        patient = Patient.objects.create(
            name="Max Mustermann", exercise=exercise, patientCode=123456
        )
        exercise_object = {
            "exerciseCode": "123456", # exercise.invitation_code
            "areas": [
                {
                    "name": "ZNA",
                    "patients": [
                        {
                            "name": patient.name,
                            "patientCode": patient.patientCode,
                            "patientId": 5,
                            "patientDatabaseId": 3, # patient.pk
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

    def handle_test_passthrough(self):
        self.send_event(
            self.TrainerOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )
