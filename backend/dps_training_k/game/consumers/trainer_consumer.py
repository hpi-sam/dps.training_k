from .abstract_consumer import AbstractConsumer
from game.models import Exercise, Patient
from django.conf import settings


class TrainerConsumer(AbstractConsumer):
    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        EXERCISE_CREATE = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_START = "exercise-start"
        EXERCISE_STOP = "exercise-stop"
        EXERCISE_PAUSE = "exercise-pause"
        EXERCISE_RESUME = "exercise-resume"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_STARTED = "exercise-start"
        EXERCISE_STOPED = "exercise-stop"
        EXERCISE_PAUSED = "exercise-pause"
        EXERCISE_RESUMED = "exercise-resume"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = None
        self.REQUESTS_MAP = {
            self.TrainerIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exercise_code",
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_CREATE: (
                self.handle_create_exercise,
            ),
            self.TrainerIncomingMessageTypes.TEST_PASSTHROUGH: (
                self.handle_test_passthrough,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_START: (
                self.handle_start_exercise,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_STOP: (
                self.handle_stop_exercise,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_PAUSE: (
                self.handle_pause_exercise,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_RESUME: (
                self.handle_resume_exercise,
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
            "exerciseCode": "a"
            * settings.INVITATION_LOGIC.code_length,  # exercise.invitation_code
            "areas": [
                {
                    "name": "ZNA",
                    "patients": [
                        {
                            "name": patient.name,
                            "patientCode": patient.patientCode,
                            "patientId": 5,
                            "patientDatabaseId": 3,  # patient.pk
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

    def handle_start_exercise(self):
        # Celery starten
        # alle Objekte mit allen Zeittracks auf 0 starten
        # Phasenübergänge schedulen
        # über NestedEventable alles stoppen
        pass

    def handle_stop_exercise(self):
        # Celery stoppen
        # alle Objekte mit allen Zeittracks auf 0 stoppen
        # Phasenübergänge stoppen
        # Labor stoppen
        # Maßnahmen stoppen
        # über NestedEventable alles stoppen
        pass

    def handle_pause_exercise(self):
        pass

    def handle_resume_exercise(self):
        pass
