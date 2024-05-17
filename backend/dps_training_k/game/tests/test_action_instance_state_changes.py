from django.test import TestCase
from game.models import ActionInstanceStateNames, ActionInstance, ActionInstanceState
from .factories import ActionInstanceFactory, LabFactory
from .mixin import TestUtilsMixin
from unittest.mock import patch


class ActionInstanceStateChangeTestCase(TestUtilsMixin, TestCase):
    def setUp(self):
        self.get_local_time_patch = patch("game.models.ActionInstance.get_local_time")
        self.get_local_time = self.get_local_time_patch.start()
        self.get_local_time.return_value = 10
        self.deactivate_notifications()
        self.deactivate_condition_checking()

    def tearDown(self):
        self.get_local_time_patch.stop()
        self.activate_notifications()
        self.activate_condition_checking()

    def test_action_instance_state_changed(self):
        """
        ActionInstanceState always create a new state object when the state name is changed.
        Two follow up states are gap free in time - one starts exactly when the other ends.
        """
        action_instance = ActionInstanceFactory(lab=LabFactory())
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
