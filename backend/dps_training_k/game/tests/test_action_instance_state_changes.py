from django.test import TestCase
from game.models import ActionInstanceStateNames, ActionInstance, ActionInstanceState
from .factories.action_instance_factory import (
    ActionInstanceFactory,
    ActionInstanceFactoryFailedState,
)
from unittest.mock import patch


class ActionInstanceStateChangeTestCase(TestCase):
    def setUp(self):
        self.get_local_time_patch = patch("game.models.ActionInstance.get_local_time")
        self.get_local_time = self.get_local_time_patch.start()
        self.get_local_time.return_value = 10

    def tearDown(self):
        self.get_local_time_patch.stop()

    def test_action_instance_state_changed(self):
        """
        ActionInstanceState always create a new state object when the state name is changed.
        Two follow up states are gap free in time - one starts exactly when the other ends.
        """
        action_instance = ActionInstanceFactory()
        number_of_states = ActionInstance.objects.count()
        action_instance._update_state(ActionInstanceStateNames.IN_PROGRESS)
        self.assertEqual(ActionInstanceState.objects.count(), number_of_states + 1)
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )
        self.assertEqual(action_instance.current_state.t_local_begin, 10)
        previous_state = action_instance.states.filter(
            name=ActionInstanceStateNames.PLANNED
        ).latest("t_local_begin")
        self.assertEqual(previous_state.t_local_end, 10)

    def test_declined_action_instance_state_change(self):
        """
        ActionInstanceState does not allow to change the state of a declined action instance.
        """
        action_instance = ActionInstanceFactoryFailedState()
        with self.assertRaises(ValueError):
            action_instance._update_state(ActionInstanceStateNames.IN_PROGRESS)
