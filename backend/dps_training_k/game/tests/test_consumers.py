from channels.testing import WebsocketCommunicator
from django.test import TestCase
from dps_training_k.asgi import application


class TrainerConsumerTestCase(TestCase):
    async def test_trainer_consumer_example_request(self):
        path = "/rooms/123/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to({"type": "example"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"type": "response", "content": "Example processed"})

        # Close the connection
        await communicator.disconnect()

class PatientConsumerTestCase(TestCase):
    async def test_trainer_consumer_example_request(self):
        path = "/rooms/123/patient/123456"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to({"type": "example"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(response, {"type": "response", "content": "exercise_code 123 & patient_code 123456"})

        # Close the connection
        await communicator.disconnect()
