from django.test import TransactionTestCase
from .mixin import TestUtilsMixin


class PatientWebSocketTest(TestUtilsMixin, TransactionTestCase):

    async def test_authenticated_websocket_connection(self):
        communicator = await self.create_patient_communicator_and_authenticate()
        # receive exercise object
        response = await communicator.receive_json_from()

        # Send a message to the WebSocket
        await communicator.send_json_to(
            {
                "messageType": "example",
                "exercise_code": "abcdef",
                "patient_code": "2",
            }
        )

        # Catch the response from available actions
        response = await communicator.receive_json_from()

        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "messageType": "response",
                "content": "exercise_code abcdef & patient_code 2",
            },
            "Unexpected response from WebSocket",
        )

        # Clean up
        await communicator.disconnect()
