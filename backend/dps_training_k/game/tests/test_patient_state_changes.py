from django.test import TestCase
from game.models import ScheduledEvent
from game.tests.factories import PatientFactory
from template.tests.factories import PatientStateFactory


class TransitionableTestCase(TestCase):

    def test_state_change_is_triggered(self):
        """
        Patient change states by first scheduling a state change and executing it successfully aftwerwards.
        """
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient.save(update_fields=["patient_state"])
        patient.schedule_state_change()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        self.assertTrue(patient.execute_state_change())

    def test_state_change_is_not_triggered_dead(self):
        """
        Patient does not change states when dead.
        """
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient_state.is_dead = True
        patient.save(update_fields=["patient_state"])
        scheduled_events = ScheduledEvent.objects.count()
        patient.schedule_state_change()
        self.assertEqual(ScheduledEvent.objects.count(), scheduled_events)

    def test_state_change_is_not_triggered_final(self):
        """
        Patient does not change states when it reached its final state
        """
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.patient_state = patient_state
        patient.save(update_fields=["patient_state"])
        patient.schedule_state_change()
        patient.execute_state_change()
        scheduled_events = ScheduledEvent.objects.count()
        patient.schedule_state_change()
        self.assertEqual(ScheduledEvent.objects.count(), scheduled_events)
