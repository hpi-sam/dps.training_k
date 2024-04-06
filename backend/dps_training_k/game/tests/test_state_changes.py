from django.test import TestCase
from game.models import ScheduledEvent
from game.tests.factories import PatientFactory
from template.tests.factories import PatientStateFactory


class TransitionableTestCase(TestCase):

    def test_state_change_is_triggered(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient.save(update_fields=["patient_state"])
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        self.assertTrue(patient.execute_state_change())

    def test_state_change_is_not_triggered_dead(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient_state.is_dead = True
        patient.patient_state = patient_state
        patient.save(update_fields=["patient_state"])
        scheduled_events = ScheduledEvent.objects.count()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), scheduled_events)

    def test_state_change_is_not_triggered_final(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient.save(update_fields=["patient_state"])
        patient.schedule_state_transition()
        patient.execute_state_change()
        scheduled_events = ScheduledEvent.objects.count()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), scheduled_events)
