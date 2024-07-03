import factory

from template.constants import ActionIDs
from template.constants import MaterialIDs
from template.models import Action
from .condition_factory import ConditionFactory


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "location",
            "relocates",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "results",
        )

    name = "Recovery Position"
    category = Action.Category.EXAMINATION
    location = Action.Location.BEDSIDE
    relocates = False
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    uuid = ActionIDs.STABILE_SEITENLAGE
    results = {
        "Hb": {
            400: "Ergebnis1",
            401: "Ergebnis2",
        },
        "BZ": {
            900: "Ergebnis1",
            901: "Ergebnis2",
        },
    }


class ActionFactoryWithEffectDuration(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "location",
            "relocates",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "results",
        )

    name = "Recovery Position"
    category = Action.Category.TREATMENT
    location = Action.Location.BEDSIDE
    relocates = False
    application_duration = 10
    effect_duration = 10
    conditions = ConditionFactory()
    uuid = ActionIDs.IV_ZUGANG
    results = {}


class ActionFactoryWithProduction(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "location",
            "relocates",
            "application_duration",
            "effect_duration",
            "conditions",
            "uuid",
            "results",
        )

    name = "Fresh Frozen Plasma (0 positiv) auftauen"
    category = Action.Category.PRODUCTION
    location = Action.Location.LAB
    relocates = False
    application_duration = 10
    effect_duration = None
    conditions = ConditionFactory()
    uuid = ActionIDs.FRESH_FROZEN_PLASMA_VORBEREITEN
    results = {
        "produced_material": {
            str(MaterialIDs.ERYTHROZYTENKONZENTRAT): 1,
        }
    }
