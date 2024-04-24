import factory
import json
from template.models import Action
from template.constants import MaterialIDs, RoleIDs, role_map
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
    conditions = json.dumps(
        {
            "required_actions": None,
            "prohibitive_actions": None,
            "material": {str(MaterialIDs.IV_ZUGANG): 1},
            "num_personnel": 1,
            "lab_devices": None,
            "area": None,
            "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
        }
    )
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
    conditions = json.dumps(
        {
            "required_actions": None,
            "prohibitive_actions": None,
            "material": {str(MaterialIDs.IV_ZUGANG): 1},
            "num_personnel": 1,
            "lab_devices": None,
            "area": None,
            "role": {role_map[RoleIDs.PFLEGEFACHKRAFT]: 1},
        }
    )
    uuid = ActionIDs.IV_Zugang
