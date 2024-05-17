from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.management import call_command
from rest_framework.authtoken.models import Token

from configuration import settings
from configuration.asgi import application
from template.models import PatientInformation
from ..models import PatientInstance, Exercise, Area
from unittest.mock import patch


class TestUtilsMixin:
    async def create_patient_communicator_and_authenticate(self):
        await sync_to_async(call_command)("patient_information")

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
        await communicator.receive_json_from()  # fetch action list

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
            "game.models.ActionInstance.check_conditions_and_block_resources"
        )
        self._deactivate_condition_checking = (
            self._deactivate_condition_checking_patch.start()
        )
        self.deactivate_condition_checking.return_value = True, None

    def activate_condition_checking(self):
        self._deactivate_condition_checking_patch.stop()
