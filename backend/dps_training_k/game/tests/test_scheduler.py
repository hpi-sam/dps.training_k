from django.test import TestCase
from django.conf import settings
from game.tests.factories import PatientFactory
from game.models import Patient, ScheduledEvent


class TempEventTest:
    def schedule_temporary_event(self):
        ScheduledEvent.create_event(
            self.exercise,
            10,
            "temporary_event_test",
            patient=self,
        )

    def temporary_event_test(self):
        return True


class EventPatient(models.patient.Patient, TempEventTest):
    pass


class EventPatientTestCase(TestCase):
    def setUp(self):
        self.patient = EventPatient.objects.create(
            name="TestPatient", patientCode=123456
        )
        CURRENT_SECONDS = lambda: 100

    def test_event_is_triggered(self):
        self.patient_blueprint = PatientFactory()
        self.patient = EventPatient.objects.create(
            name=self.patient_blueprint.name,
            exercise=self.patient_blueprint.exercise,
            patientCode=self.patient_blueprint.patientCode,
        )
