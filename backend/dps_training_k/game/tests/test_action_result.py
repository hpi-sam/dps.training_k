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
from template.tests.factories import (
    ActionFactoryWithProduction,
    ExaminationCodesData,
    EmptyPatientStateFactory,
)
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
        action_instance = ActionInstanceFactory(
            patient_instance=PatientFactory(
                patient_state=EmptyPatientStateFactory(
                    examination_codes=ExaminationCodesData.generate()
                )
            )
        )
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
            "BZ: Ergebnis2\nHb: Ergebnis1",
        )

    def test_action_production(self):
        """
        a production action creates material instances as specified in Action.results.produced_material.value in the area of the action instance.
        """
        action = ActionFactoryWithProduction()
        action_instance = ActionInstanceFactory(
            template=action, lab=LabFactory(), destination_area=AreaFactory()
        )
        Material.objects.update_or_create(
            uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            name="Erythrozytenkonzentrat 0 pos.",
            category=Material.Category.BLOOD,
            is_reusable=False,
        )
        count_before = MaterialInstance.objects.filter(
            template__uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            area=action_instance.destination_area,
        ).count()
        action_instance._application_finished()
        count_after = MaterialInstance.objects.filter(
            template__uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            area=action_instance.destination_area,
        ).count()
        self.assertEqual(count_before + 1, count_after)


class ActionResultIntegrationTestCase(TestUtilsMixin, TransactionTestCase):
    def timezone_from_timestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def test_action_production_lifecycle(self):
        """
        Integration Test: If production action is finished, material instances are created according to the results.produced_material field.
        """
        call_command("import_actions")
        call_command("import_material")
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(0)
        self.deactivate_notifications()
        self.deactivate_condition_checking()
        action_template = Action.objects.get(name="Erythrozytenkonzentrat erwärmen")
        area = AreaFactory()
        lab = LabFactory()
        action_instance = ActionInstance.create(
            action_template,
            lab=lab,
            destination_area=area,
        )
        action_instance.try_application()
        self.assertRaises(
            MaterialInstance.DoesNotExist,
            MaterialInstance.objects.get,
            template__uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
            area=area,
        )
        settings.CURRENT_TIME = lambda: self.timezone_from_timestamp(
            action_template.application_duration + 1
        )
        check_for_updates()
        self.assertIsNotNone(
            MaterialInstance.objects.get(
                template__uuid=MaterialIDs.ERYTHROZYTENKONZENTRAT,
                area=area,
            )
        )
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()
        self.activate_condition_checking()

    @patch(
        "game.channel_notifications.MaterialInstanceDispatcher._notify_exercise_update"
    )
    def test_action_production_notification(self, _notify_exercise_update):
        """
        Integration Test: If production action is finished, a notification is sent to the consumer.
        """

        call_command("import_actions")
        call_command("import_material")
        action_template = Action.objects.get(name="Erythrozytenkonzentrat erwärmen")
        area = AreaFactory()
        lab = LabFactory()
        action_instance = ActionInstance.create(
            action_template,
            lab=lab,
            destination_area=area,
        )
        action_instance._application_finished()
        self.assertEqual(_notify_exercise_update.call_count, 1)
