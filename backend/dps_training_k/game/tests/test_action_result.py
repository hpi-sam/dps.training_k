import asyncio
import datetime
from unittest.mock import patch

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, TransactionTestCase
from django.utils import timezone

from game.models import ActionInstanceStateNames, MaterialInstance
from game.tasks import check_for_updates
from game.tests.factories import (
    ActionInstanceFactory,
    PatientFactory,
    LabFactory,
    AreaFactory,
    ActionInstance,
)
from template.constants import MaterialIDs
from template.models import Material, Action
from template.tests.factories.action_factory import ActionFactoryWithProduction
from .mixin import TestUtilsMixin


class ActionResultTestCase(TestUtilsMixin, TestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)
        self.deactivate_notifications()
        self.deactivate_condition_checking()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()
        self.activate_condition_checking()

    def test_action_examination_result(self):
        """
        an action of category examination has a result that is set by translating the result codes in its results field.
        """
        action_instance = ActionInstanceFactory(patient_instance=PatientFactory())
        action_instance._start_application()
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(10)
        check_for_updates()
        action_instance.refresh_from_db()
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.FINISHED)
        self.assertEqual(
            action_instance.result,
            "Recovery Position wurde durchgeführt",
        )

    def test_action_production(self):
        """
        a production action creates material instances as specified in Action.results.produced_material.value in the area of the action instance.
        """
        action = ActionFactoryWithProduction()
        action_instance = ActionInstanceFactory(
            template=action, lab=LabFactory(), area=AreaFactory()
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        count_before = MaterialInstance.objects.filter(
            template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            area=action_instance.area,
        ).count()
        action_instance._application_finished()
        count_after = MaterialInstance.objects.filter(
            template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            area=action_instance.area,
        ).count()
        self.assertEqual(count_before + 1, count_after)


class ActionResultIntegrationTestCase(TestUtilsMixin, TransactionTestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)
        self.deactivate_notifications()
        self.deactivate_condition_checking()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()
        self.activate_condition_checking()

    def test_action_production_lifecycle(self):
        """
        Integration Test: If production action is finished, material instances are created according to the results.produced_material field.
        """
        call_command("minimal_actions")
        call_command("minimal_material")
        action_template = Action.objects.get(
            name="Fresh Frozen Plasma (0 positiv) auftauen"
        )
        area = AreaFactory()
        lab = LabFactory()
        action_instance = ActionInstance.create(
            action_template,
            lab=lab,
            area=area,
        )
        action_instance.try_application()
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(20)
        self.assertRaises(
            MaterialInstance.DoesNotExist,
            MaterialInstance.objects.get,
            template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            area=area,
        )
        check_for_updates()
        self.assertIsNotNone(
            MaterialInstance.objects.get(
                template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
                area=area,
            )
        )

    @patch(
        "game.channel_notifications.MaterialInstanceDispatcher._notify_exercise_update"
    )
    def test_action_production_notification(self, _notify_exercise_update):
        """
        Integration Test: If production action is finished, a notification is send to the consumer.
        """

        call_command("minimal_actions")
        call_command("minimal_material")
        action_template = Action.objects.get(
            name="Fresh Frozen Plasma (0 positiv) auftauen"
        )
        area = AreaFactory()
        lab = LabFactory()
        action_instance = ActionInstance.create(
            action_template,
            lab=lab,
            area=area,
        )
        action_instance._application_finished()
        self.assertEqual(_notify_exercise_update.call_count, 1)


class ActionCreationTestCase(TestUtilsMixin, TransactionTestCase):
    def setUp(self):
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        ActionFactoryWithProduction(application_duration=0)
        self.deactivate_notifications()
        self.deactivate_condition_checking()

    def tearDown(self):
        self.activate_notifications()
        self.activate_condition_checking()

    @patch("game.models.MaterialInstance.generate_materials")
    async def test_action_production_dispatching(self, generate_materials):
        """
        when a production action was added via websockets, check whether action instance steps through the production routine
        inside action_instance._application_finished.

        """
        communicator = await self.create_patient_communicator_and_authenticate()
        await self.skip_initial_fetching(communicator)

        # Send a message to the WebSocket
        await communicator.send_json_to(
            {
                "messageType": "action-add",
                "actionName": "Fresh Frozen Plasma (0 positiv) auftauen",
            }
        )
        await asyncio.sleep(0.1)
        await sync_to_async(check_for_updates)()
        self.assertEqual(generate_materials.call_count, 1)
