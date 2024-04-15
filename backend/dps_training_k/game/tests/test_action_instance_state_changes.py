from django.test import TestCase
from game.models import ActionInstanceStateNames
from .factories.action_instance_factory import (
    ActionInstanceFactory,
    ActionInstanceFactoryFailedState,
)
from unittest.mock import patch


class ActionInstanceStateChangeTestCase(TestCase):

    @patch("game.models.ActionInstance.get_local_time")
    def test_action_instance_state_changed(self, get_local_time):
        action_instance = ActionInstanceFactory()
        number_of_states = action_instance.objects.count()
        get_local_time.return_value = 10
        action_instance._updadate_state(ActionInstanceStateNames.IN_PROGRESS)
        self.assertEqual(action_instance.objects.count(), number_of_states + 1)
        self.assertEqual(
            action_instance.state.name, ActionInstanceStateNames.IN_PROGRESS
        )
        self.assertEqual(action_instance.state.t_local_begin, 10)
        previous_state = self.objects.filter(
            state__name=ActionInstanceStateNames.PLANNED
        ).latest("t_local_begin")
        self.assertEqual(previous_state.t_local_end, 10)

    @patch("game.models.ActionInstance.get_local_time")
    def test_declined_action_instance_state_change(self, get_local_time):
        get_local_time.return_value = 10
        action_instance = ActionInstanceFactoryFailedState()
        with self.assertRaises(ValueError):
            action_instance._update_state(ActionInstanceStateNames.IN_PROGRESS)
