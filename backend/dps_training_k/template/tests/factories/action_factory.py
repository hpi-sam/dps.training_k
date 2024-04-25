import factory
import json
from .condition_factory import ConditionFactory
from template.models import Action
from template.constants import MaterialIDs, RoleIDs, role_map
from template.constants import ActionIDs
from template.management.commands.minimal_resources import Command


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "success_result",
        )

    uuid = ActionIDs.STABILE_SEITENLAGE
    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    success_result = json.dumps(
        {"material": {str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 2}}
    )

    @factory.post_generation
    def create_resources(self, create, extracted, **kwargs):
        if not create:
            return
        Command.create_resources()


class ActionFactoryWithEffectDuration(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "success_result",
        )

    uuid = ActionIDs.STABILE_SEITENLAGE
    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    effect_duration = 10
    conditions = ConditionFactory()
    success_result = json.dumps(
        {"material": {str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 2}}
    )

    @factory.post_generation
    def create_resources(self, create, extracted, **kwargs):
        if not create:
            return
        Command.create_resources()
