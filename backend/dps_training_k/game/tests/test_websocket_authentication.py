from django.core.management import call_command
from django.test import TransactionTestCase

from .mixin import TestUtilsMixin


class PatientWebSocketTest(TestUtilsMixin, TransactionTestCase):
    def setUp(self):
        call_command("patient_information")

    async def test_authenticated_websocket_connection(self):
        communicator = await self.create_patient_communicator_and_authenticate()

        await communicator.receive_json_from()  # catch exercise object

        # Send a message to the WebSocket
        await communicator.send_json_to(
            {
                "messageType": "example",
                "exerciseId": self.exercise.exercise_frontend_id,
                "patientId": self.patient.patient_frontend_id,
            }
        )

        await communicator.receive_json_from()  # Catch available actions
        await communicator.receive_json_from()  # Catch available patients

        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {
                "messageType": "response",
                "content": "exerciseId "
                + self.exercise.exercise_frontend_id
                + " & patientId "
                + self.patient.patient_frontend_id,
            },
            "Unexpected response from WebSocket",
        )

        # Clean up
        await communicator.disconnect()
