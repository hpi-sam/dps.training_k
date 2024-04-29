import factory
from template.models import Action
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
            "results",
        )

    name = "Recovery Position"
    category = Action.Category.EXAMINATION
    application_duration = 10
    effect_duration = None
    conditions = JSONFactory({"to_be_replaced_after_actual_condition_checking": None})
    uuid = ActionIDs.STABILE_SEITENLAGE
    results = {
        "Hb": [
            {ActionResultIDs.HB420: "Ergebnis1"},
            {ActionResultIDs.HB430: "Ergebnis2"},
        ],
        "BZ": [
            {ActionResultIDs.BZ920: "Ergebnis1"},
            {ActionResultIDs.BZ930: "Ergebnis2"},
        ],
    }


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
    conditions = JSONFactory({"to_be_replaced_after_actual_condition_checking": None})
    uuid = ActionIDs.IV_ZUGANG
    results = None

