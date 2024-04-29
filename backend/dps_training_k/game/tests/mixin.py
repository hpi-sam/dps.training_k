from game.models import User
from .factories import PatientFactory
from rest_framework.authtoken.models import Token
from channels.testing import WebsocketCommunicator
from configuration.asgi import application
from asgiref.sync import sync_to_async


class TestUtilsMixin:
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
