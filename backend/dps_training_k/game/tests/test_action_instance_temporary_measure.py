from django.test import TestCase
from .factories.action_instance_factory import ActionInstanceFactoryWithEffectDuration
from .factories.patient_factory import PatientFactory
from game.models import ActionInstanceStateNames
from django.utils import timezone
import datetime
from django.conf import settings
from game.tasks import check_for_updates


class ActionInstanceTemporaryMeasureTestCase(TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup

    def test_action_instance_temporary_measure(self):
        """
        test whether action instance goes from IN_PROGESS to IN_EFFECT to EXPIRED state
        in application_duration and effect_duration respectively.
        """
        action_instance = ActionInstanceFactoryWithEffectDuration(
            patient_instance=PatientFactory()
        )
        action_instance._start_application()
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        action_instance.refresh_from_db()
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.IN_EFFECT)
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(20)
        check_for_updates()
        action_instance.refresh_from_db()
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.EXPIRED)
