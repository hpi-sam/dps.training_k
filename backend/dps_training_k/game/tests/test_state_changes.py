from django.test import TestCase
from game.models import ScheduledEvent
from game.tests.factories import PatientFactory
from template.tests.factories import PatientStateFactory


class TransitionableTestCase(TestCase):

    def state_change_is_triggered(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1).generate()
        patient.patient_state = patient_state
        patient.save()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        self.assertTrue(patient.execute_state_transition())

    def state_change_is_not_triggered(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(0, 0)
        patient.patient_state = patient_state
        patient.save()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), 1)
        self.assertFalse(patient.execute_state_transition())

    def state_change_is_not_triggered_dead(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(2, 2)

        patient_state.is_dead = True
        patient.patient_state = patient_state
        patient.save()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), 0)

    def state_change_is_not_triggered_final(self):
        patient = PatientFactory()
        patient_state = PatientStateFactory(1, 1)
        patient.save()
        patient.execute_state_transition()
        patient.schedule_state_transition()
        self.assertEqual(ScheduledEvent.objects.count(), 0)

    # patient mit phasechange
    # geht in die nächste phase
    # bei maximum passiert nichts
    # bei dead passiert nichts
