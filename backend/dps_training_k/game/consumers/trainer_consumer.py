from urllib.parse import parse_qs

from configuration import settings
from game.models import Area, Exercise, Personnel, PatientInstance, MaterialInstance, LogEntry, Lab
from template.constants import MaterialIDs
from template.models import Patient, Material
from .abstract_consumer import AbstractConsumer
from ..channel_notifications import ChannelNotifier, LogEntryDispatcher
from ..serializers import LogEntrySerializer
from template.serializers import PatientSerializer


class TrainerConsumer(AbstractConsumer):
    """
    for general functionality @see AbstractConsumer
    """

    class TrainerIncomingMessageTypes:
        AREA_ADD = "area-add"
        AREA_DELETE = "area-delete"
        AREA_RENAME = "area-rename"
        EXAMPLE = "example"
        EXERCISE_CREATE = "exercise-create"
        EXERCISE_END = "exercise-end"
        EXERCISE_START = "exercise-start"
        MATERIAL_ADD = "material-add"
        MATERIAL_DELETE = "material-delete"
        PATIENT_ADD = "patient-add"
        PATIENT_DELETE = "patient-delete"
        PATIENT_RENAME = "patient-rename"
        PATIENT_UPDATE = "patient-update"
        PATIENT_GET_TEMPLATE = "patient-get-template"
        PERSONNEL_ADD = "personnel-add"
        PERSONNEL_DELETE = "personnel-delete"
        PERSONNEL_RENAME = "personnel-rename"

    class TrainerOutgoingMessageTypes:
        LOG_UPDATE = "log-update"
        RESPONSE = "response"
        PATIENT_TEMPLATE = "patient-template"

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
            self.TrainerIncomingMessageTypes.AREA_RENAME: (
                self.handle_rename_area,
                "areaId",
                "areaName",
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
            self.TrainerIncomingMessageTypes.PATIENT_RENAME: (
                self.handle_rename_patient,
                "patientId",
                "patientName",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_UPDATE: (
                self.handle_update_patient,
                "patientId",
                "code",
            ),
            self.TrainerIncomingMessageTypes.PATIENT_GET_TEMPLATE: (
                self.handle_get_patient_template,
                "patientCode",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_ADD: (
                self.handle_add_personnel,
                "areaId",
                "personnelName",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_DELETE: (
                self.handle_delete_personnel,
                "personnelId",
            ),
            self.TrainerIncomingMessageTypes.PERSONNEL_RENAME: (
                self.handle_rename_personnel,
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

    def handle_rename_area(self, exercise, area_id, area_name):
        area = Area.objects.get(id=area_id, exercise_id=exercise.id)
        area.name = area_name
        area.save(update_fields=["name"])

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

    def handle_start_exercise(self, exercise):
        exercise.start_exercise()

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
            if not material.patient_instance:
                material.delete()
            else:
                self.send_failure(
                    "Material ist einem Patienten zugewiesen und kann deswegen nicht gelöscht werden. Bitte gebe zuerst das Material frei oder "
                    "lösche den Patienten."
                )
        except MaterialInstance.DoesNotExist:
            self.send_failure(
                f"No material found with the id '{materialId}'",
            )

    def handle_add_patient(self, _, areaId, patientName, code):
        try:
            area = Area.objects.get(id=areaId)
            patient_template = Patient.objects.get(info__code=code)
            
            # a patient in state 551 starts "beatmet" and therefore needs a "Beatmungsgerät"
            '''
            if patient_information.start_status == 551:
                try:
                    material_instances = MaterialInstance.objects.filter(
                        template__uuid__in=[
                            MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
                            MaterialIDs.BEATMUNGSGERAET_STATIONAER,
                        ]
                    )
                    # find a "Beatmungsgerät" that has not been assigned to a patient but is in same area as the patient
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
                            message="Dieser Patient benötigt bereits zu Beginn ein Beatmungsgerät."
                        )
                except (
                    MaterialInstance.DoesNotExist
                ):  # catches no material_instance matching filter
                    self.send_failure(
                        message="Dieser Patient benötigt bereits zu Beginn ein Beatmungsgerät."
                    )
            else:
            '''
            PatientInstance.objects.create(
                name=patientName,
                patient_template=patient_template,
                patient_state_id=patient_template.get_initial_state_id(),
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

    def handle_delete_patient(self, _, patientFrontendId):
        try:
            patient = PatientInstance.objects.get(frontend_id=patientFrontendId)
            if patient.static_information.start_status == 551:
                self._unassign_beatmungsgeraet(patient)
            patient.delete()

        except PatientInstance.DoesNotExist:
            self.send_failure(
                f"No patient found with the patientId '{patientFrontendId}'",
            )

    def handle_rename_patient(self, exercise, patient_id, patient_name):
        patient = PatientInstance.objects.get(
            frontend_id=patient_id, exercise_id=exercise.id
        )
        patient.name = patient_name
        patient.save(update_fields=["name"])

    def handle_update_patient(self, _, patient_frontend_id, code):
        patient = PatientInstance.objects.get(frontend_id=patient_frontend_id)
        new_patient_template = Patient.objects.get(info__code=code)
        '''
        if patient.static_information.start_status == 551:
            self._unassign_beatmungsgeraet(patient)

        # if new start state is 551, try to assign a "Beatmungsgerät"
        if new_patient_information.start_status == 551:
            try:
                ventilators = MaterialInstance.objects.filter(
                    template__uuid__in=[
                        MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
                        MaterialIDs.BEATMUNGSGERAET_STATIONAER,
                    ]
                )
                # find a "Beatmungsgerät" that has not been assigned to a patient but is in same area as the patient
                succeeded = False
                for ventilator in ventilators:
                    if ventilator.attached_instance() == patient.area:
                        succeeded = True
                        break
                if succeeded:
                    patient.static_information = new_patient_information
                    patient.save(update_fields=["static_information"])
                    # While Python does know the concept of scopes, one can still use the variables after the for loop. So what happens here is that
                    # the for loop loops until it finds a desired ventilator and then breaks as to not overwrite the current instance.
                    ventilator.try_moving_to(patient)
                else:
                    self.send_failure(
                        message="Dieser Patient benötigt bereits zu Beginn ein Beatmungsgerät."
                    )

            except:
                self.send_failure(
                    message="Dieser Patient benötigt bereits zu Beginn ein Beatmungsgerät."
                )
        else:
        '''
        patient.patient_template = new_patient_template
        patient.save(update_fields=["patient_template"])
        
    def handle_get_patient_template(self, _, patient_code):
        patient_template = Patient.objects.all().filter(info__code=patient_code).values()[0]
        self.send_event(
            self.TrainerOutgoingMessageTypes.PATIENT_TEMPLATE,
            patientTemplate=PatientSerializer(patient_template).data,
        )

    def handle_add_personnel(self, _, areaId, personnel_name):
        try:
            area = Area.objects.get(id=areaId)
            Personnel.create_personnel(area=area, name=personnel_name)
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
            if not personnel.patient_instance:
                personnel.delete()
            else:
                self.send_failure(
                    "Personal ist einem Patienten zugewiesen und kann deswegen nicht gelöscht werden. Bitte gebe zuerst das Personal frei oder "
                    "lösche den Patienten."
                )
        except Personnel.DoesNotExist:
            self.send_failure(
                f"No personnel found with the id '{personnel_id}'",
            )

    def handle_rename_personnel(self, _, personnel_id, personnel_name):
        personnel = Personnel.objects.get(id=personnel_id)
        personnel.name = personnel_name
        personnel.save(update_fields=["name"])

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

    def _unassign_beatmungsgeraet(self, patient):
        material_instances = MaterialInstance.objects.filter(
            template__uuid__in=[
                MaterialIDs.BEATMUNGSGERAET_TRAGBAR,
                MaterialIDs.BEATMUNGSGERAET_STATIONAER,
            ]
        )
        # find the "Beatmungsgerät" that has been assigned to the patient
        for material_instance in material_instances:
            if material_instance.attached_instance() == patient:
                break
        # unassign "Beatmungsgerät"
        material_instance.try_moving_to(patient.area)

    # ------------------------------------------------------------------------------------------------------------------------------------------------
    # Events triggered internally by channel notifications
    # ------------------------------------------------------------------------------------------------------------------------------------------------
    def log_update_event(self, event):
        log_entry = LogEntry.objects.get(id=event["log_entry_id"])

        self.send_event(
            self.TrainerOutgoingMessageTypes.LOG_UPDATE,
            logEntries=[LogEntrySerializer(log_entry).data],
        )
