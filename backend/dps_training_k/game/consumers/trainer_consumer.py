from configuration import settings
from game.models import Area
from game.models import Exercise, Personnel, PatientInstance, MaterialInstance, LogEntry
from template.models import PatientInformation, Material
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier, LogEntryDispatcher
from ..serializers import LogEntrySerializer
from template.constants import MaterialIDs

class TrainerConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class TrainerIncomingMessageTypes:
        EXAMPLE = "example"
        EXERCISE_CREATE = "exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        EXERCISE_START = "exercise-start"
        EXERCISE_END = "exercise-end"
        EXERCISE_PAUSE = "exercise-pause"
        EXERCISE_RESUME = "exercise-resume"
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        PATIENT_ADD = "patient-add"
        PATIENT_UPDATE = "patient-update"
        PATIENT_DELETE = "patient-delete"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_UPDATE = "personnel-update"
        MATERIAL_ADD = "material-add"
        MATERIAL_DELETE = "material-delete"

    class TrainerOutgoingMessageTypes:
        RESPONSE = "response"
        EXERCISE_CREATED = "trainer-exercise-create"
        TEST_PASSTHROUGH = "test-passthrough"
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        LOG_UPDATE = "log-update"

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
            self.TrainerIncomingMessageTypes.EXERCISE_END: (self.handle_end_exercise,),
            self.TrainerIncomingMessageTypes.EXERCISE_PAUSE: (
                self.handle_pause_exercise,
            ),
            self.TrainerIncomingMessageTypes.EXERCISE_RESUME: (
                self.handle_resume_exercise,
            ),
            self.TrainerIncomingMessageTypes.AREA_ADD: (self.handle_add_area,),
            self.TrainerIncomingMessageTypes.AREA_DELETE: (
                self.handle_delete_area,
                "areaId",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_ADD: (
                self.handle_add_patient,
                "areaId",
                "patientName",
                "code",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_UPDATE: (
                self.handle_update_patient,
                "patientId",
                "patientName",
                "code",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_DELETE: (
                self.handle_delete_patient,
                "patientId",
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
            self.TrainerIncomingMessageTypes.MATERIAL_ADD: (
                self.handle_add_material,
                "areaId",
                "materialName",
            ),
            self.TrainerIncomingMessageTypes.MATERIAL_DELETE: (
                self.handle_delete_material,
                "materialId",
            ),
        }

    def connect(self):
        self.accept()
        self.send_available_patients()
        self.send_available_materials()
        if self.exercise:
            self.send_past_logs()

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # API Methods, open to client.
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_example(self, exercise, exercise_frontend_id):
        self.exercise_frontend_id = exercise_frontend_id
        self.send_event(
            self.TrainerOutgoingMessageTypes.RESPONSE,
            content=f"exerciseId {self.exercise_frontend_id}",
        )

    # here, the exercise argument is None
    def handle_create_exercise(self, exercise):
        self.exercise = Exercise.createExercise()
        self.exercise_frontend_id = self.exercise.frontend_id
        self._send_exercise(self.exercise)
        self.subscribe(ChannelNotifier.get_group_name(self.exercise))
        self.subscribe(LogEntryDispatcher.get_group_name(self.exercise))

    def handle_test_passthrough(self, exercise):
        self.send_event(
            self.TrainerOutgoingMessageTypes.TEST_PASSTHROUGH,
            message="received test event",
        )

    def handle_start_exercise(self, exercise):
        owned_patients = PatientInstance.objects.filter(exercise=exercise)
        for time_offset, patient in enumerate(owned_patients):
            # we don't start all patients at once to balance out the work for our celery workers
            patient.schedule_state_change(time_offset)
        exercise.update_state(Exercise.StateTypes.RUNNING)

    def handle_end_exercise(self, exercise):
        exercise.update_state(Exercise.StateTypes.FINISHED)
        exercise.delete()

    def handle_pause_exercise(self, exercise):
        pass

    def handle_resume_exercise(self, exercise):
        pass

    def handle_add_area(self, exercise):
        Area.create_area(name="Bereich", exercise=exercise, isPaused=False)

    def handle_delete_area(self, _, areaId):
        try:
            area = Area.objects.get(pk=areaId)
            area.delete()
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the pk '{areaId}'",
            )

    def handle_add_patient(self, _, areaId, patientName, code):
        try:
            area = Area.objects.get(pk=areaId)
            patient_information = PatientInformation.objects.get(code=code)
            if patient_information.start_status == 551:
                try:
                    material_instances = MaterialInstance.objects.filter(template__uuid=MaterialIDs.BEATMUNGSGERAET)
                    print(material_instances)
                    succeeded = False
                    for material_instance in material_instances:
                        print(material_instance.attached_instance())
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
                    else: # catches case where no material_instance was in patients area
                        self.send_failure(message="Es fehlt ein Beatmungsgerät um den Patienten im Zustand 551 starten zu lassen.")
                except MaterialInstance.DoesNotExist: # catches no material_instance matching filter
                    self.send_failure(message="Es fehlt ein Beatmungsgerät um den Patienten im Zustand 551 starten zu lassen.")
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
                f"No area found with the pk '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the pk '{areaId}'",
            )

    def handle_update_patient(self, exercise, patientFrontendId, patientName, code):
        patient = PatientInstance.objects.get(frontend_id=patientFrontendId)
        patient_information = PatientInformation.objects.get(code=code)
        if not patient.static_information.start_status == 551:
            patient.name = patientName
            patient.static_information = patient_information
            patient.save(update_fields=["name", "static_information"])
        else:
            self.send_failure(message="Patienten mit Startstatus 551 können momentan keinen neuen Code zugewiesen bekommen.")

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
            area = Area.objects.get(pk=areaId)
            Personnel.create_personnel(area=area, name="Personal")
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the pk '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the pk '{areaId}'",
            )

    def handle_update_personnel(self, _, personnelId, personnelName):
        personnel = Personnel.objects.get(id=personnelId)
        personnel.name = personnelName
        personnel.save()

    def handle_delete_personnel(self, _, personnel_id):
        try:
            personnel = Personnel.objects.get(id=personnel_id)
            personnel.delete()
        except Personnel.DoesNotExist:
            self.send_failure(
                f"No personnel found with the pk '{personnel_id}'",
            )

    def handle_add_material(self, _, areaId, materialName):
        try:
            area = Area.objects.get(id=areaId)
            template = Material.objects.get(name=materialName)
            MaterialInstance.objects.create(template=template, area=area)
        except Area.DoesNotExist:
            self.send_failure(
                f"No area found with the pk '{areaId}'",
            )
        except Area.MultipleObjectsReturned:
            self.send_failure(
                f"Multiple areas found with the pk '{areaId}'",
            )

    def handle_delete_material(self, _, materialId):
        try:
            material = MaterialInstance.objects.get(id=materialId)
            material.delete()
        except MaterialInstance.DoesNotExist:
            self.send_failure(
                f"No material found with the pk '{materialId}'",
            )

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
        log_entry = LogEntry.objects.get(pk=event["log_entry_pk"])

        self.send_event(
            self.TrainerOutgoingMessageTypes.LOG_UPDATE,
            logEntries=[LogEntrySerializer(log_entry).data],
        )
