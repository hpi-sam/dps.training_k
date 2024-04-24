from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase

from configuration.asgi import application


class TrainerConsumerTestCase(TransactionTestCase):
    maxDiff = None

    async def test_trainer_consumer_example_request(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.receive_json_from()  # catch available patients

        # Send an "example" request type message to the server
        await communicator.send_json_to({"messageType": "example", "exerciseId": "123"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(
            response, {"messageType": "response", "content": "exerciseId 123"}
        )

        # Close the connection
        await communicator.disconnect()

    async def test_trainer_handle_create_exercise(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.receive_json_from()  # catch available patients

        # Send an "example" request type message to the server
        await communicator.send_json_to({"messageType": "exercise-create"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()

        self.assertEqual("exercise", response["messageType"])

        # Close the connection
        await communicator.disconnect()

    async def test_trainer_consumer_test_passthrough_request(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.receive_json_from()  # catch available patients

        # Send an "example" request type message to the server
        await communicator.send_json_to({"messageType": "test-passthrough"})

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(
            response,
            {"messageType": "test-passthrough", "message": "received test event"},
        )

        # Close the connection
        await communicator.disconnect()
