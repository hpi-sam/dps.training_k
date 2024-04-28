from game.models import Area
from game.models import Exercise, Personnel, PatientInstance, InventoryEntry
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier
from template.models import Resource


class TrainerConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        EXERCISE_CREATE = "exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_START = "exercise-start"
        EXERCISE_STOP = "exercise-end"
        EXERCISE_PAUSE = "exercise-pause"
        EXERCISE_RESUME = "exercise-resume"
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_UPDATE = "personnel-update"
        MATERIAL_ADD = "material-add"
        MATERIAL_DELETE = "material-delete"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-created"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_STARTED = "exercise-started"
        EXERCISE_END = "exercise-ended"
        EXERCISE_PAUSED = "exercise-paused"
        EXERCISE_RESUMED = "exercise-resumed"
        AREA_ADD = "area-added"
        AREA_DELETE = "area-deleted"

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
            self.TrainerIncomingMessageTypes.MATERIAL_ADD: (
                self.handle_add_material,
                "areaName",
                "materialName",
            ),
            self.TrainerIncomingMessageTypes.MATERIAL_DELETE: (
                self.handle_delete_material,
                "materialId",
            ),
        }

    def connect(self):
        self.accept()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_example(self, exercise_code):
        self.exercise_code = exercise_code
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            content=f"exercise_code {self.exercise_code}",
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

    def handle_add_material(self, areaName, materialName):
        area = Area.objects.get(name=areaName, exercise=self.exercise)
        material = Resource.objects.get(name=materialName)
        area.consuming_inventory.change_resource(material, 1)

    def handle_delete_material(self, materialId):
        inventoryEntry = InventoryEntry.objects.get(id=materialId)
        material = inventoryEntry.resource
        inventory = inventoryEntry.inventory
        inventory.change_resource(material, -1)
