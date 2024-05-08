from django.test import TestCase
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
import datetime
from django.conf import settings
from game.tasks import check_for_updates
from template.models import Material
from template.constants import MaterialIDs


class ActionResultTestCase(TestUtilsMixin, TestCase):
    def timezoneFromTimestamp(self, timestamp):
        return timezone.make_aware(datetime.datetime.fromtimestamp(timestamp))

    def setUp(self):
        self.variable_backup = settings.CURRENT_TIME
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(0)
        self.deactivate_notifications()

    def tearDown(self):
        settings.CURRENT_TIME = self.variable_backup
        self.activate_notifications()

    def test_action_examination_result(self):
        action_instance = ActionInstanceFactory(patient_instance=PatientFactory())
        action_instance._start_application()
        self.assertEqual(
            action_instance.state_name, ActionInstanceStateNames.IN_PROGRESS
        )
        settings.CURRENT_TIME = lambda: self.timezoneFromTimestamp(10)
        check_for_updates()
        action_instance.refresh_from_db()
        self.assertEqual(action_instance.state_name, ActionInstanceStateNames.FINISHED)
        self.assertEqual(
            action_instance.result,
            "Recovery Position Ergebnis: Hb: Ergebnis1 BZ: Ergebnis2",
        )

    def test_action_production(self):
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
