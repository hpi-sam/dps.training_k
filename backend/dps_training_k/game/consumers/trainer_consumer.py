from game.models import Area
from game.models import Exercise, Personnel, Patient
from .abstract_consumer import AbstractConsumer


class TrainerConsumer(AbstractConsumer):
    """
    This class is responsible for DECODING messages from the frontend(user==trainer) into method calls and
    ENCODING events from the backend into JSONs to send to the frontend. When encoding events this also implies
    deciding what part of the event should be sent to the frontend(filtering).
    """

    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        EXERCISE_CREATE = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_START = "exercise-start"
        EXERCISE_STOP = "exercise-stop"
        EXERCISE_PAUSE = "exercise-pause"
        EXERCISE_RESUME = "exercise-resume"
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_UPDATE = "personnel-update"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_UPDATE = "personnel-update"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_STARTED = "exercise-start"
        EXERCISE_STOPED = "exercise-stop"
        EXERCISE_PAUSED = "exercise-pause"
        EXERCISE_RESUMED = "exercise-resume"
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exercise_code = None
        self.exercise = None
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
            self.TrainerIncomingMessageTypes.AREA_ADD: (self.handle_add_area,),
            self.TrainerIncomingMessageTypes.AREA_DELETE: (
                self.handle_delete_area,
                "areaName",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_ADD: (
                self.handle_add_personnel,
                "areaName",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_DELETE: (
                self.handle_delete_personnel,
                "personnelId",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_UPDATE: (
                self.handle_update_personnel,
                "personnelId",
                "personnelName",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_ADD: (
                self.handle_add_personnel,
                "areaName",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_DELETE: (
                self.handle_delete_personnel,
                "personnelId",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_UPDATE: (
                self.handle_update_personnel,
                "personnelId",
                "personnelName",
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
        self.exercise = Exercise.createExercise()
        self._send_exercise(self.exercise)

    def handle_test_passthrough(self):
        self.send_event(
            self.TrainerOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_start_exercise(self):
        owned_patients = Patient.objects.filter(exercise=self.exercise)
        [patient.schedule_state_transition() for patient in owned_patients]

    def handle_stop_exercise(self):
        # Stop Celery
        # Stop all objects with all time tracks
        # Stop phase transitions
        # Stop laboratory
        # Stop measures
        # Stop everything using NestedEventable
        pass

    def handle_pause_exercise(self):
        pass

    def handle_resume_exercise(self):
        pass

    def handle_add_area(self):
        Area.create_area(name="Bereich", exercise=self.exercise, isPaused=False)
        # TODO: send update to all subscribers

    def handle_delete_area(self, areaName):
        Area.objects.filter(name=areaName).delete()
        # TODO: send update to all subscribers

    def handle_add_personnel(self, areaName):
        try:
            area = Area.objects.get(name=areaName)
            Personnel.objects.create(area=area)
            self._send_exercise(self.exercise)
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the name '{areaName}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the name '{areaName}'",
            )

    def handle_delete_personnel(self, personnelId):
        Personnel.objects.filter(id=personnelId).delete()
        self._send_exercise(self.exercise)

    def handle_update_personnel(self, personnelId, personnelName):
        personnel = Personnel.objects.get(id=personnelId)
        personnel.name = personnelName
        personnel.save()
        self._send_exercise(self.exercise)

    def handle_add_personnel(self, areaName):
        try:
            area = Area.objects.get(name=areaName)
            Personnel.objects.create(area=area)
            self._send_exercise(self.exercise)
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the name '{areaName}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the name '{areaName}'",
            )

    def handle_delete_personnel(self, personnelId):
        Personnel.objects.filter(id=personnelId).delete()
        self._send_exercise(self.exercise)

    def handle_update_personnel(self, personnelId, personnelName):
        personnel = Personnel.objects.get(id=personnelId)
        personnel.name = personnelName
        personnel.save()
        self._send_exercise(self.exercise)
