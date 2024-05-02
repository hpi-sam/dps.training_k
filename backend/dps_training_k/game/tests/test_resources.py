import json
from django.test import TestCase
from unittest.mock import patch
from .factories import PatientActionInstanceFactory
from template.models import Resource, Action
from template.tests.factories import ConditionFactory, ActionFactory
from template.constants import MaterialIDs


class TestResourcesTestCase(TestCase):
    def setUp(self):
        self.application_status_patch = patch(
            "template.models.Action.application_status"
        )
        self.application_status = self.application_status_patch.start()
        self.application_status.return_value = True, None
        self.conditions = ConditionFactory(
            material={str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 1}
        )
        self.success_result = json.dumps(
            {"material": {str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 1}}
        )
        self.action_template = ActionFactory(
            conditions=self.conditions, success_result=self.success_result
        )
        self.action_instance = PatientActionInstanceFactory(
            action_template=self.action_template
        )
        self.resource = Resource.objects.get(
            uuid=MaterialIDs.CONCENTRATED_RED_CELLS_0_POS
        )
        self.inventory = self.action_instance.place_of_application().consuming_inventory

    def tearDown(self):
        self.application_status_patch.stop()

    def test_resources_inventory_synchronized_consuming(self):
        "When actions need resources, the inventory is reduced by the needed amount"
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._consume_resources()
        self.assertEqual(
            self.inventory.resource_stock(self.resource), initial_amount - 1
        )

        self.action_template.category = Action.Category.LAB
        self.action_template.save(update_fields=["category"])
        self.inventory = self.action_instance.place_of_application().consuming_inventory
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._consume_resources()
        self.assertEqual(
            self.inventory.resource_stock(self.resource), initial_amount - 1
        )

    def test_resources_returned_after_application(self):
        "When resource is returnable it gets returned"
        self.resource.is_returnable = False
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._return_applicable_resources()
        self.assertEqual(self.inventory.resource_stock(self.resource), initial_amount)

        self.resource.is_returnable = True
        self.resource.save(update_fields=["is_returnable"])
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._return_applicable_resources()
        self.assertEqual(
            self.inventory.resource_stock(self.resource), initial_amount + 1
        )

    def test_resource_production(self):
        "When action has resources inside its success result, they get produced after application"
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._produce_resources()
        self.assertEqual(
            self.inventory.resource_stock(self.resource), initial_amount + 1
        )

        self.action_template.success_result = json.dumps({})
        initial_amount = self.inventory.resource_stock(self.resource)
        self.action_instance._produce_resources()
        self.assertEqual(self.inventory.resource_stock(self.resource), initial_amount)
