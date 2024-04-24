from game.models import Area
from game.models import Exercise, Personnel, PatientInstance
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier


class TrainerConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        EXERCISE_CREATE = "exercise-create"
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
        self.exercise_frontend_id = None
        self.exercise = None
        self.REQUESTS_MAP = {
            self.TrainerIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exerciseId",
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
        }

    def connect(self):
        self.accept()
        self.send_available_patients()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_example(self, exercise_frontend_id):
        self.exercise_frontend_id = exercise_frontend_id
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id}",
        )

    def handle_create_exercise(self):
        self.exercise = Exercise.createExercise()
        self._send_exercise(self.exercise)
        self.subscribe(ChannelNotifier.get_group_name(self.exercise))

    def handle_test_passthrough(self):
        self.send_event(
            self.TrainerOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_start_exercise(self):
        owned_patients = PatientInstance.objects.filter(exercise=self.exercise)
        [patient.schedule_state_change() for patient in owned_patients]

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

    def handle_delete_area(self, areaName):
        try:
            area = Area.objects.get(name=areaName)
            area.delete()
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the name '{areaName}'",
            )

    def handle_add_personnel(self, areaName):
        try:
            area = Area.objects.get(name=areaName)
            Personnel.objects.create(area=area)
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the name '{areaName}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the name '{areaName}'",
            )

    def handle_delete_personnel(self, personnel_id):
        try:
            personnel = Personnel.objects.get(id=personnel_id)
            personnel.delete()
        except Personnel.DoesNotExist:
            self.send_failure(
                f"No personnel found with the pk '{personnel_id}'",
            )

    def handle_update_personnel(self, personnelId, personnelName):
        personnel = Personnel.objects.get(id=personnelId)
        personnel.name = personnelName
        personnel.save()
