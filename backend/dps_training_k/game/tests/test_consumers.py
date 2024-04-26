import json
import asyncio

from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from game.models import ActionInstance
from channels.db import database_sync_to_async
from configuration.asgi import application
from django.core.management import call_command
from .mixin import TestUtilsMixin


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
    def action_instance_exists(self, action_id):
        return ActionInstance.objects.filter(action_template__id=action_id).exists()

    async def test_patient_consumer_add_action(self):
        communicator = await self.create_patient_communicator_and_authenticate()

        # receive exercise object
        exercise = await communicator.receive_json_from()
        # receive available actions
        available_actions = await communicator.receive_json_from()
        # extract first available actions' id
        availableActions = available_actions["availableActions"]
        actions_json = json.loads(availableActions)
        first_action = actions_json["actions"][0]
        first_action_json = json.loads(first_action)
        action_id = first_action_json["actionId"]

        await communicator.send_json_to(
            {
                "messageType": "action-add",
                "actionId": action_id,
            }
        )
        # it needs some time for processing, will hang otherwise (assuming it deadlocks)
        await asyncio.sleep(1)

        exists = await self.action_instance_exists(action_id)
        self.assertTrue(
            exists, "ActionInstance was not created with the given action_template ID."
        )

        await communicator.disconnect()
