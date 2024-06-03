from unittest.mock import patch

from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.management import call_command
from rest_framework.authtoken.models import Token

from configuration import settings
from configuration.asgi import application
from template.models import PatientInformation
from ..models import PatientInstance, Exercise, Area


class TestUtilsMixin:
    async def create_patient_communicator_and_authenticate(self):
        await sync_to_async(call_command)("patient_information")
        await sync_to_async(call_command)("loaddata", "patient_state_1004.json")

        self.exercise = await sync_to_async(Exercise.createExercise)()
        self.patient_information = await sync_to_async(PatientInformation.objects.get)(
            code=1004
        )
        area = await sync_to_async(Area.create_area)(
            name="Test Bereich", exercise=self.exercise, isPaused=False
        )
        self.patient = await sync_to_async(PatientInstance.objects.create)(
            name="Max Mustermann",
            static_information=self.patient_information,
            exercise=self.exercise,
            area=area,
            frontend_id=settings.ID_GENERATOR.get_patient_frontend_id(),
        )
        self.token, _ = await sync_to_async(Token.objects.get_or_create)(
            user=self.patient.user
        )

        communicator = WebsocketCommunicator(
            application=application, path=f"/ws/patient/?token={self.token.key}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "Failed to connect to WebSocket")

        return communicator

    async def skip_initial_fetching(self, communicator):
        await communicator.receive_json_from()  # fetch exercise
        await communicator.receive_json_from()  # fetch actions
        await communicator.receive_json_from()  # fetch patients

    def deactivate_notifications(self):
        @classmethod
        def custom_save_and_notify(cls, obj, changes, save_origin, *args, **kwargs):
            save_origin.save(*args, **kwargs)

        self._deactivate_notifications_patch = patch(
            "game.channel_notifications.ChannelNotifier.save_and_notify",
            new=custom_save_and_notify,
        )
        self._deactivate_notifications_patch.start()

    def activate_notifications(self):
        self._deactivate_notifications_patch.stop()

    def deactivate_condition_checking(self):
        self._deactivate_condition_checking_patch = patch(
            "game.models.ActionInstance._try_acquiring_resources"
        )
        self._deactivate_condition_checking = (
            self._deactivate_condition_checking_patch.start()
        )
        self._deactivate_condition_checking.return_value = ([], "", True)

    def activate_condition_checking(self):
        self._deactivate_condition_checking_patch.stop()

    def deactivate_logging(self):
        self._deactivate_logging_patch = patch(
            "game.channel_notifications.LogEntryDispatcher.dispatch_event"
        )
        self._deactivate_logging = self._deactivate_logging_patch.start()

    def activate_logging(self):
        self._deactivate_logging_patch.stop()

    def deactivate_live_updates(self):
        self._deactivate_live_updates_patch = patch(
            "game.channel_notifications.ChannelNotifier._notify_action_check_update"
        )
        self._deactivate_live_updates = self._deactivate_live_updates_patch.start()

    def activate_live_updates(self):
        self._deactivate_live_updates_patch.stop()

    def deactivate_results(self):
        self._deactivate_result_patch = patch(
            "template.models.Action.get_result", return_value=None
        )
        self._deactivate_result = self._deactivate_result_patch.start()

    def activate_results(self):
        self._deactivate_result_patch.stop()

    def deactivate_moving(self):
        self._deactivate_moving_patch = patch(
            "game.models.PatientInstance._perform_move"
        )
        self._deactivate_moving = self._deactivate_moving_patch.start()

    def activate_moving(self):
        self._deactivate_moving_patch.stop()

    def deactivate_relocating(self):
        self._deactivate_relocating_patch = patch(
            "game.models.ActionInstance._try_relocating", patch=(True, "")
        )
        self._deactivate_relocating = self._deactivate_relocating_patch.start()
        self._check_relocating_patch = patch(
            "game.models.ActionInstance._check_relocating",
            return_value=(True, False, ""),
        )
        self._check_relocating = self._check_relocating_patch.start()

    def activate_relocating(self):
        self._deactivate_relocating_patch.stop()
        self._check_relocating_patch.stop()
