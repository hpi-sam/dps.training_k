from django.test import TestCase, TransactionTestCase
from game.tests.factories import (
    ActionInstanceFactory,
    PatientFactory,
    LabFactory,
    AreaFactory,
)
from .mixin import TestUtilsMixin
from template.tests.factories.action_factory import ActionFactoryWithProduction
from game.models import ActionInstanceStateNames, MaterialInstance
from django.utils import timezone
import datetime, unittest.mock as mock, asyncio
from django.conf import settings
from game.tasks import check_for_updates
from template.models import Material
from template.constants import MaterialIDs
from asgiref.sync import sync_to_async


class ActionResultTestCase(TestUtilsMixin, TestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)
        self.deactivate_notifications()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()

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
            "Recovery Position Ergebnis: Hb: Ergebnis1 BZ: Ergebnis2",
        )

    def test_action_production(self):
        """
        a production action creates material instances as specified in Action.results.produced_material.value in the area of the action instance.
        """
        action = ActionFactoryWithProduction()
        action_instance = ActionInstanceFactory(
            action_template=action, lab=LabFactory(), area=AreaFactory()
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        count_before = MaterialInstance.objects.filter(
            material_template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            area=action_instance.area,
        ).count()
        action_instance._application_finished()
        count_after = MaterialInstance.objects.filter(
            material_template__uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            area=action_instance.area,
        ).count()
        self.assertEqual(count_before + 1, count_after)


class ActionCreationTestCase(TestUtilsMixin, TransactionTestCase):
    def setUp(self):
        Material.objects.update_or_create(
            uuid=MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS,
            name="Enthrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        ActionFactoryWithProduction(application_duration=0)

    @mock.patch("game.models.MaterialInstance.generate_materials")
    async def test_action_production_creation(self, generate_materials):
        """
        when a production action is added, check whether action instance steps through the production routine
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
