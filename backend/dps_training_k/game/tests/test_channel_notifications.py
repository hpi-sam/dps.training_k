from django.test import TestCase
from .factories import (
    PatientActionInstanceFactory,
    ActionInstanceStateFactory,
    PatientFactory,
)
import game.channel_notifications as cn
from game.models import ActionInstanceStateNames
from unittest.mock import patch


class ChannelNotifierTestCase(TestCase):
    @patch.object(cn.ChannelNotifier, "_notify_group")
    def test_action_dispatcher(self, notify_group_mock):
        action_instance = PatientActionInstanceFactory()
        action_instance.current_state = ActionInstanceStateFactory(
            name=ActionInstanceStateNames.FINISHED
        )
        previous_function_calls = notify_group_mock.call_count
        action_instance.save(update_fields=["current_state"])
        self.assertEqual(notify_group_mock.call_count, previous_function_calls + 1)

    @patch.object(cn.ChannelNotifier, "_notify_group")
    def test_patient_dispatcher(self, notify_group_mock):
        patient_instance = PatientFactory()
        previous_function_calls = notify_group_mock.call_count
        patient_instance.save(update_fields=["patient_state"])
        self.assertEqual(notify_group_mock.call_count, previous_function_calls + 1)
