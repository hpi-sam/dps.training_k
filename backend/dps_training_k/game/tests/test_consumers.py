from channels.testing import WebsocketCommunicator
from django.test import TestCase
from dps_training_k.asgi import application


class TrainerConsumerTestCase(TestCase):
    maxDiff = None
    async def test_trainer_consumer_example_request(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to({"type": "example", "exercise_code": "123"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"type": "response", "content": "exercise_code 123"})

        # Close the connection
        await communicator.disconnect()
    
    async def test_trainer_handle_create_exercise(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to({"type": "trainer-exercise-create"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        content = {
            "exerciseCode": 123456,
            "areas": [
                {
                    "name": "ZNA",
                    "patients": [
                        {
                            "name": "Max Mustermann",
                            "patientCode": 123456,
                            "patientId": 5,
                            "patientDatabaseId": 3,
                        }
                    ],
                    "personnel": [
                        {
                            "name": "Hanna Schulz",
                            "role": "Arzt",
                            "personnelDatabaseId": 6,
                        }
                    ],
                    "devices": [{"name": "EKG", "deviceDatabaseId": 15}],
                }
            ],
        }
        self.assertEqual(response, {"type": "trainer-exercise-create", "exercise": content})

        # Close the connection
        await communicator.disconnect()


class PatientConsumerTestCase(TestCase):
    async def test_trainer_consumer_example_request(self):
        path = "/ws/patient/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to(
            {"type": "example", "exercise_code": "123", "patient_code": "123456"}
        )

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {"type": "response", "content": "exercise_code 123 & patient_code 123456"},
        )

        # Close the connection
        await communicator.disconnect()
