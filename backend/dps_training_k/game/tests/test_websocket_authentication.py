from django.test import TransactionTestCase
from .mixin import TestUtilsMixin


class PatientWebSocketTest(TestUtilsMixin, TransactionTestCase):

    async def test_authenticated_websocket_connection(self):
        communicator = await self.create_patient_communicator_and_authenticate()

        await communicator.receive_json_from()  # catch exercise object

        # Send a message to the WebSocket
        await communicator.send_json_to(
            {
                "messageType": "example",
                "exerciseId": "abcdef",
                "patientId": "2",
            }
        )

        await communicator.receive_json_from()  # Catch available actions
        await communicator.receive_json_from()  # Catch available patients

        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "messageType": "response",
                "content": "exerciseId abcdef & patientId 2",
            },
            "Unexpected response from WebSocket",
        )

        # Clean up
        await communicator.disconnect()
