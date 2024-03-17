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

        # Send an "example" request type message to the server
        await communicator.send_json_to(
            {"messageType": "example", "exercise_code": "123"}
        )

        # Receive and test the response from the server
        response = await communicator.receive_json_from()
        self.assertEqual(
            response, {"messageType": "response", "content": "exercise_code 123"}
        )

        # Close the connection
        await communicator.disconnect()

    async def test_trainer_handle_create_exercise(self):
        path = "/ws/trainer/"
        communicator = WebsocketCommunicator(application, path)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an "example" request type message to the server
        await communicator.send_json_to({"messageType": "trainer-exercise-create"})

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


class PatientConsumerTestCase(TransactionTestCase):
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
            {"messageType": "test-passthrough", "message": "received test event"},
        )

        # Close the connection
        await communicator.disconnect()
