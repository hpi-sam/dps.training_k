import factory, json
from template.models import Action
from .JSON_factory import JSONFactory
from .condition_factory import ConditionFactory
from template.constants import MaterialIDs
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
            "results",
        )

    name = "Recovery Position"
    category = Action.Category.EXAMINATION
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    uuid = ActionIDs.STABILE_SEITENLAGE
    results = json.dumps(
        {
            "Hb": [
                {ActionResultIDs.HB420: "Ergebnis1"},
                {ActionResultIDs.HB430: "Ergebnis2"},
            ],
            "BZ": [
                {ActionResultIDs.BZ920: "Ergebnis1"},
                {ActionResultIDs.BZ930: "Ergebnis2"},
            ],
        }
    )


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
            "results",
        )

    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    effect_duration = 10
    conditions = ConditionFactory()
    uuid = ActionIDs.IV_ZUGANG
    results = json.dumps({})


class ActionFactoryWithProduction(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "results",
        )

    name = "Fresh Frozen Plasma (0 positiv) auftauen"
    category = Action.Category.PRODUCTION
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    uuid = ActionIDs.FRESH_FROZEN_PLASMA_AUFTAUEN
    results = json.dumps(
        {
            "produced_material": {
                str(MaterialIDs.ENTHROZYTENKONZENTRAT_0_POS): 1,
            }
        }
    )
