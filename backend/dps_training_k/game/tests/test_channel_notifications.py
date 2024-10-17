from unittest.mock import patch

from django.test import TestCase

import game.channel_notifications as cn
from game.models import ActionInstanceStateNames
from .factories import (
    ActionInstanceFactory,
    ActionInstanceStateFactory,
    PatientFactory,
)
from .mixin import TestUtilsMixin


class ChannelNotifierTestCase(TestUtilsMixin, TestCase):
    def setUp(self):
        self.deactivate_logging()
        self.deactivate_live_updates()

    def tearDown(self):
        self.activate_logging()
        self.activate_live_updates()

    @patch.object(cn.ChannelNotifier, "_notify_group")
    def test_action_dispatcher(self, notify_group_mock):
        action_instance = ActionInstanceFactory(patient_instance=PatientFactory())
        action_instance.current_state = ActionInstanceStateFactory(
            name=ActionInstanceStateNames.FINISHED
        )
        previous_function_calls = notify_group_mock.call_count
        action_instance.save(update_fields=["current_state"])

        self.assertEqual(
            notify_group_mock.call_count, previous_function_calls + 2
        )  # action list & continuous variables

    @patch.object(cn.ChannelNotifier, "_notify_group")
    def test_patient_dispatcher(self, notify_group_mock):
        patient_instance = PatientFactory()
        previous_function_calls = notify_group_mock.call_count
        patient_instance.save(update_fields=["patient_state"])

        self.assertEqual(
            notify_group_mock.call_count, previous_function_calls + 2
        )  # state & continuous variables
