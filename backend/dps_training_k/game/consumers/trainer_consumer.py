from urllib.parse import parse_qs

from configuration import settings
from game.models import Area
from game.models import Exercise, Personnel, PatientInstance, MaterialInstance, LogEntry
from template.models import PatientInformation, Material
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier, LogEntryDispatcher
from ..serializers import LogEntrySerializer
from template.constants import MaterialIDs
from game.models import Lab



class TrainerConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class TrainerIncomingMessageTypes:
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        EXAMPLE = "example"
        EXERCISE_CREATE = "exercise-create"
        EXERCISE_END = "exercise-end"
        EXERCISE_START = "exercise-start"
        MATERIAL_ADD = "material-add"
        MATERIAL_DELETE = "material-delete"
        PATIENT_ADD = "patient-add"
        PATIENT_DELETE = "patient-delete"
        PATIENT_UPDATE = "patient-update"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_UPDATE = "personnel-update"

    class TrainerOutgoingMessageTypes:
        EXERCISE_CREATED = "trainer-exercise-create"
        LOG_UPDATE = "log-update"
        RESPONSE = "response"
        TEST_PASSTHROUGH = "test-passthrough"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_arguments = [
            lambda: (
                Exercise.objects.get(frontend_id=self.exercise_frontend_id)
                if self.exercise_frontend_id
                else None
            )
        ]
        self.exercise_frontend_id = None
        self.exercise = None
        trainer_request_map = {
            self.TrainerIncomingMessageTypes.AREA_ADD: (self.handle_add_area,),
            self.TrainerIncomingMessageTypes.AREA_DELETE: (
                self.handle_delete_area,
                "areaId",
            ),
            self.TrainerIncomingMessageTypes.EXAMPLE: (
                self.handle_example,
                "exerciseId",
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_CREATE: (
                self.handle_create_exercise,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_END: (self.handle_end_exercise,),
            self.TrainerIncomingMessageTypes.EXERCISE_START: (
                self.handle_start_exercise,
            ),
            self.TrainerIncomingMessageTypes.MATERIAL_ADD: (
                self.handle_add_material,
                "areaId",
                "materialName",
            ),
            self.TrainerIncomingMessageTypes.MATERIAL_DELETE: (
                self.handle_delete_material,
                "materialId",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_ADD: (
                self.handle_add_patient,
                "areaId",
                "patientName",
                "code",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_DELETE: (
                self.handle_delete_patient,
                "patientId",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_UPDATE: (
                self.handle_update_patient,
                "patientId",
                "patientName",
                "code",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_ADD: (
                self.handle_add_personnel,
                "areaId",
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
        self.REQUESTS_MAP.update(trainer_request_map)

    def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        success, _ = self.authenticate(token)
        if success:
            self.accept()
            self.send_available_patients()
            self.send_available_materials()
            if self.exercise:
                self.send_past_logs()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # These methods are not allowed to be called directly. If you want to call them from the backend, go via self.receive_json()
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_add_area(self, exercise):
        Area.create_area(name="Bereich", exercise=exercise, isPaused=False)

    def handle_delete_area(self, _, areaId):
        try:
            area = Area.objects.get(id=areaId)
            area.delete()
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the id '{areaId}'",
            )

    def handle_example(self, exercise, exercise_frontend_id):
        self.exercise_frontend_id = exercise_frontend_id
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id}",
        )

    # here, the exercise argument is None
    def handle_create_exercise(self, exercise):
        if Exercise.objects.filter(trainer=self.user).exists():
            self.exercise = Exercise.objects.get(trainer=self.user)
        else:
            self.exercise = Exercise.createExercise(self.user)
        self.exercise_frontend_id = self.exercise.frontend_id
        Lab.objects.get(exercise=self.exercise).create_basic_devices()
        self._send_exercise(self.exercise)
        self.subscribe(ChannelNotifier.get_group_name(self.exercise))
        self.subscribe(LogEntryDispatcher.get_group_name(self.exercise))

    def handle_end_exercise(self, exercise):
        exercise.update_state(Exercise.StateTypes.FINISHED)
        exercise.delete()

    def handle_start_exercise(self, exercise):
        owned_patients = PatientInstance.objects.filter(exercise=exercise)
        for time_offset, patient in enumerate(owned_patients):
            # we don't start all patients at once to balance out the work for our celery workers
            patient.schedule_state_change(time_offset)
        exercise.update_state(Exercise.StateTypes.RUNNING)

    def handle_add_material(self, _, areaId, materialName):
        try:
            area = Area.objects.get(id=areaId)
            template = Material.objects.get(name=materialName)
            MaterialInstance.objects.create(template=template, area=area)
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the id '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the id '{areaId}'",
            )

    def handle_delete_material(self, _, materialId):
        try:
            material = MaterialInstance.objects.get(id=materialId)
            material.delete()
        except MaterialInstance.DoesNotExist:
            self.send_failure(
                f"No material found with the id '{materialId}'",
            )

    def handle_add_patient(self, _, areaId, patientName, code):
        try:
            area = Area.objects.get(id=areaId)
            patient_information = PatientInformation.objects.get(code=code)
            if patient_information.start_status == 551:
                try:
                    material_instances = MaterialInstance.objects.filter(
                        template__uuid__in=[MaterialIDs.BEATMUNGSGERAET_TRAGBAR, MaterialIDs.BEATMUNGSGERAET_STATIONAER]
                    )
                    succeeded = False
                    for material_instance in material_instances:
                        if material_instance.attached_instance() == area:
                            succeeded = True
                            break

                    if succeeded:
                        patient_instance = PatientInstance.objects.create(
                            name=patientName,
                            static_information=patient_information,
                            exercise=area.exercise,
                            area=area,
                            frontend_id=settings.ID_GENERATOR.get_patient_frontend_id(),
                        )
                        material_instance.try_moving_to(patient_instance)
                    else:  # catches case where no material_instance was in patients area
                        self.send_failure(
                            message="Es fehlt ein Beatmungsgerät um den Patienten im Zustand 551 starten zu lassen."
                        )
                except (
                    MaterialInstance.DoesNotExist
                ):  # catches no material_instance matching filter
                    self.send_failure(
                        message="Es fehlt ein Beatmungsgerät um den Patienten im Zustand 551 starten zu lassen."
                    )
            else:
                patient_instance = PatientInstance.objects.create(
                    name=patientName,
                    static_information=patient_information,
                    exercise=area.exercise,
                    area=area,
                    frontend_id=settings.ID_GENERATOR.get_patient_frontend_id(),
                )

        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the id '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the id '{areaId}'",
            )

    def handle_update_patient(self, exercise, patientFrontendId, patientName, code):
        patient = PatientInstance.objects.get(frontend_id=patientFrontendId)
        patient_information = PatientInformation.objects.get(code=code)
        if not patient.static_information.start_status == 551:
            patient.name = patientName
            patient.static_information = patient_information
            patient.save(update_fields=["name", "static_information"])
        else:
            self.send_failure(
                message="Patienten mit Startstatus 551 können momentan keinen neuen Code zugewiesen bekommen."
            )

    def handle_delete_patient(self, exercise, patientFrontendId):
        try:
            patient = PatientInstance.objects.get(frontend_id=patientFrontendId)
            patient.delete()
        except PatientInstance.DoesNotExist:
            self.send_failure(
                f"No patient found with the patientId '{patientFrontendId}'",
            )

    def handle_add_personnel(self, _, areaId):
        try:
            area = Area.objects.get(id=areaId)
            Personnel.create_personnel(area=area, name="Personal")
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the id '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the id '{areaId}'",
            )

    def handle_delete_personnel(self, _, personnel_id):
        try:
            personnel = Personnel.objects.get(id=personnel_id)
            personnel.delete()
        except Personnel.DoesNotExist:
            self.send_failure(
                f"No personnel found with the id '{personnel_id}'",
            )

    def handle_update_personnel(self, _, personnelId, personnelName):
        personnel = Personnel.objects.get(id=personnelId)
        personnel.name = personnelName
        personnel.save()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # methods used internally
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def send_past_logs(self, exercise):
        log_entry_objects = LogEntry.objects.filter(exercise=exercise)
        log_entry_objects = filter(
            lambda log_entry: log_entry.is_valid(), log_entry_objects
        )
        if not log_entry_objects:
            return
        log_entry_dicts = [
            LogEntrySerializer(log_entry).data for log_entry in log_entry_objects
        ]
        self.send_event(
            self.TrainerOutgoingMessageTypes.LOG_UPDATE, logEntries=log_entry_dicts
        )

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def log_update_event(self, event):
        log_entry = LogEntry.objects.get(id=event["log_entry_id"])

        self.send_event(
            self.TrainerOutgoingMessageTypes.LOG_UPDATE,
            logEntries=[LogEntrySerializer(log_entry).data],
        )
