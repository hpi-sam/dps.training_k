import factory
from template.models import Action
from .JSON_factory import JSONFactory


class ActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Action
        django_get_or_create = (
            "name",
            "category",
            "application_duration",
            "conditions",
        )

    name = "Recovery Position"
    category = Action.Category.TREATMENT
    application_duration = 10
    conditions = JSONFactory({"to_be_replaced_after_actual_condition_checking": None})
