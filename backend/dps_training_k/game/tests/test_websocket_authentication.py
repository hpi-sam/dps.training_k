from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from rest_framework.authtoken.models import Token

from configuration.asgi import application
from game.models import User
from .factories import PatientFactory


class PatientWebSocketTest(TransactionTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(username="2", password="abcdef")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.patient = PatientFactory()

    async def test_authenticated_websocket_connection(self):
        print("Startet test_authenticated_websocket_connection")
        communicator = WebsocketCommunicator(
            application=application, path=f"/ws/patient/?token={self.token.key}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "Failed to connect to WebSocket")

        response = await communicator.receive_json_from()

        await communicator.send_json_to(
            {
                "messageType": "example",
                "exercise_code": "abcdef",
                "patient_code": "2",
            }
        )

        response = (
            await communicator.receive_json_from()
        )  # Catch the response from available actions

        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "messageType": "response",
                "content": "exercise_code abcdef & patient_code 2",
            },
            "Unexpected response from WebSocket",
        )

        await communicator.disconnect()
        print("Finished test_authenticated_websocket_connection")
