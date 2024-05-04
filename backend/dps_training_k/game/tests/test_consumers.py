import asyncio

from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.management import call_command
from django.test import TransactionTestCase

from configuration.asgi import application
from game.models import ActionInstance
from .mixin import TestUtilsMixin


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


class PatientConsumerTestCase(TestUtilsMixin, TransactionTestCase):
    maxDiff = None

    def setUp(self):
        call_command("minimal_actions")

    @database_sync_to_async
    def action_instance_exists(self, action_name):
        return ActionInstance.objects.filter(action_template__name=action_name).exists()

    async def test_patient_consumer_add_action(self):
        communicator = await self.create_patient_communicator_and_authenticate()

        # receive exercise object
        exercise = await communicator.receive_json_from()
        # receive available actions
        available_actions = await communicator.receive_json_from()
        # extract first available actions' id
        action_name = available_actions["availableActions"][0]["actionName"]

        await communicator.send_json_to(
            {
                "messageType": "action-add",
                "actionName": action_name,
            }
        )
        # it needs some time for processing, will hang otherwise (assuming it deadlocks)
        await asyncio.sleep(1)

        exists = await self.action_instance_exists(action_name)
        self.assertTrue(
            exists, "ActionInstance was not created with the given action_template ID."
        )

        await communicator.disconnect()
