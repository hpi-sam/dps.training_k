import factory
import json
from .condition_factory import ConditionFactory
from template.models import Action
from template.constants import ActionIDs, MaterialIDs, RoleIDs, role_map
from template.management.commands.minimal_resources import Command

from .JSON_factory import JSONFactory
from template.constants import ActionIDs, ActionResultIDs

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
    category = Action.Category.EXAMINATION
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    success_result = json.dumps(
        {"material": {str(MaterialIDs.CONCENTRATED_RED_CELLS_0_POS): 2}}
    )
    # success_result = {
    #     "Hb": [
    #         {ActionResultIDs.HB420: "Ergebnis1"},
    #         {ActionResultIDs.HB430: "Ergebnis2"},
    #     ],
    #     "BZ": [
    #         {ActionResultIDs.BZ920: "Ergebnis1"},
    #         {ActionResultIDs.BZ930: "Ergebnis2"},
    #     ],
    # } # ToDo: add examination action factory

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
