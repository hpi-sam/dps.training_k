import factory
from template.models import Action
from .JSON_factory import JSONFactory
from template.constants import ActionIDs


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
        )

    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    effect_duration = None
    conditions = JSONFactory({"to_be_replaced_after_actual_condition_checking": None})
    uuid = ActionIDs.STABILE_SEITENLAGE


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
        )

    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    effect_duration = 10
    conditions = JSONFactory({"to_be_replaced_after_actual_condition_checking": None})
    uuid = ActionIDs.IV_Zugang
