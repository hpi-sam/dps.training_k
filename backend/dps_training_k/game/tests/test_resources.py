import json
from django.test import TestCase
from unittest.mock import patch
from .factories import (
    PatientActionInstanceFactory,
    LabActionInstanceFactory,
    AreaFactory,
)
from template.models import Resource, Action
from template.tests.factories import ConditionFactory, ActionFactory
from template.constants import MaterialIDs


class TestResourcesPatientTestCase(TestCase):
    def setUp(self):
        self.conditions = ConditionFactory(
            material={str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 2}
        )
        self.action_template = ActionFactory(conditions=self.conditions)
        self.action_instance = PatientActionInstanceFactory(
            action_template=self.action_template
        )
        self.resource = Resource.objects.get(
            uuid=MaterialIDs.CONCENTRATED_RED_CELLS_0_POS
        )
        self.area_inventory = self.action_instance.area.inventory
        self.patient_inventory = self.action_instance.patient_instance.inventory

    def test_resources_inventories_synchronized(self):
        "When patient actions need resources, they get transfered from the areas inventory"
        self.area_inventory.change_resource(self.resource, 1)
        self.patient_inventory.change_resource(self.resource, 1)
        self.resource.is_returnable = True
        self.resource.save(update_fields=["is_returnable"])
        self.action_instance._consume_resources()
        self.assertEqual(self.area_inventory.resource_stock(self.resource), 0)
        self.assertEqual(self.patient_inventory.resource_stock(self.resource), 2)
        self.resource.is_returnable = False
        self.resource.save(update_fields=["is_returnable"])

    def test_resources_get_destroyed(self):
        "When actions need destroyable resources, they get destroyed on start of application"
        self.resource.is_returnable = False
        self.resource.save(update_fields=["is_returnable"])
        self.patient_inventory.change_resource(self.resource, 2)
        self.action_instance._consume_resources()
        self.assertEqual(self.patient_inventory.resource_stock(self.resource), 0)


class TestResourcesLabTestCase(TestCase):
    def setUp(self):
        self.success_result = json.dumps(
            {"material": {str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 1}}
        )
        self.conditions = ConditionFactory(
            material={str(MaterialIDs.BLOOD_DEFROSTING_SLOT): 1}
        )
        self.action_template = ActionFactory(
            conditions=self.conditions, success_result=self.success_result
        )
        self.action_instance = LabActionInstanceFactory(
            action_template=self.action_template,
            area=AreaFactory(),
        )
        self.resource = Resource.objects.get(uuid=MaterialIDs.BLOOD_DEFROSTING_SLOT)
        self.produced_resource = Resource.objects.get(
            uuid=MaterialIDs.CONCENTRATED_RED_CELLS_0_POS
        )
        self.lab_inventory = self.action_instance.lab.inventory
        self.area_inventory = self.action_instance.area.inventory

    def test_resources_consumed(self):
        "When lab action is applied, resources get consumed from it's own inventory"
        self.lab_inventory.change_resource(self.resource, 1)
        self.action_instance._consume_resources()
        self.assertEqual(self.lab_inventory.resource_stock(self.resource), 0)

    def test_resources_returned_after_application(self):
        "When a resource is returnable it gets returned after it left InProgress State"
        self.resource.is_returnable = False
        self.resource.save(update_fields=["is_returnable"])
        initial_amount = self.lab_inventory.resource_stock(self.resource)
        self.action_instance._return_applicable_resources()
        self.assertEqual(
            self.lab_inventory.resource_stock(self.resource), initial_amount
        )

        self.resource.is_returnable = True
        self.resource.save(update_fields=["is_returnable"])
        initial_amount = self.lab_inventory.resource_stock(self.resource)
        self.action_instance._return_applicable_resources()
        self.assertEqual(
            self.lab_inventory.resource_stock(self.resource), initial_amount + 1
        )

    def test_resource_production(self):
        "When an action has resources inside its success result, they get produced after application"
        initial_amount = self.area_inventory.resource_stock(self.produced_resource)
        resource_recepie = self.action_instance.action_template.produced_resources()
        self.action_instance._produce_resources(resource_recepie)
        self.assertEqual(
            self.area_inventory.resource_stock(self.produced_resource),
            initial_amount + 1,
        )
