from django.test import TestCase
from .setupable import TestSetupable
from .factories.action_instance_factory import ActionInstanceFactoryWithEffectDuration
from game.models import ActionInstanceStateNames
from django.utils import timezone
import datetime
from django.conf import settings
from unittest.mock import patch
from game.tasks import check_for_updates


class ActionInstanceTemporaryMeasureTestCase(TestSetupable, TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)
        self.deactivate_resources()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_resources()

    def test_action_instance_temporary_measure(self):
        action_instance = ActionInstanceFactoryWithEffectDuration()
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
