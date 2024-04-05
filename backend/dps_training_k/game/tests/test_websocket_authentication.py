from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from rest_framework.authtoken.models import Token

from configuration.asgi import application
from game.models import User
from .factories import PatientFactory


class PatientWebSocketTest(TransactionTestCase):
    def setUp(self):
        super().setUp()
        # Create a user and token for testing
        self.user = User.objects.create_user(username="6", password="123456")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.patient = PatientFactory()

    """
    async def test_authenticated_websocket_connection(self):
        # Connect to the WebSocket
        communicator = WebsocketCommunicator(
            application=application, path=f"/ws/patient/?token={self.token.key}"
        )
        connected, _ = await communicator.connect()
        self.assertTrue(connected, "Failed to connect to WebSocket")

        # receive exercise object
        response = await communicator.receive_json_from()

        # Send a message to the WebSocket
        await communicator.send_json_to(
            {
                "messageType": "example",
                "exercise_code": "123456",
                "patient_code": "6",
            }
        )

        # Receive the response from the WebSocket
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "messageType": "response",
                "content": "exercise_code 123456 & patient_code 6",
            },
            "Unexpected response from WebSocket",
        )

        # Clean up
        await communicator.disconnect()
"""
