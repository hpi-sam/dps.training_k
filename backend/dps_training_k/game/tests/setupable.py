from unittest.mock import patch
from game.models import User
from .factories import PatientFactory
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator
from configuration.asgi import application
from asgiref.sync import sync_to_async


class TestSetupable:
    def deactivate_resources(self):
        self._consume_resources_patch_patient = patch(
            "game.models.PatientActionInstance._consume_resources"
        )
        self._consume_resources_patch_lab = patch(
            "game.models.LabActionInstance._consume_resources"
        )
        self._application_finished_strategy_patch_lab = patch(
            "game.models.LabActionInstance._application_finished_strategy"
        )
        self._consume_resources_patient = self._consume_resources_patch_patient.start()
        self._consume_resources_lab = self._consume_resources_patch_lab.start()
        self._application_finished_strategy_lab = (
            self._application_finished_strategy_patch_lab.start()
        )
        self._consume_resources_patient.return_value = None
        self._consume_resources_lab.return_value = None
        self._application_finished_strategy_lab.return_value = None

    def activate_resources(self):
        self._consume_resources_patch_patient.stop()
        self._consume_resources_patch_lab.stop()
        self._application_finished_strategy_patch_lab.stop()

    async def create_patient_communicator_and_authenticate(self):
        self.user = await sync_to_async(User.objects.create_user)(
            username="2", password="abcdef"
        )
        self.token, _ = await sync_to_async(Token.objects.get_or_create)(user=self.user)
        self.patient = await sync_to_async(PatientFactory)()

        communicator = WebsocketCommunicator(
            application=application, path=f"/ws/patient/?token={self.token.key}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "Failed to connect to WebSocket")

        return communicator
