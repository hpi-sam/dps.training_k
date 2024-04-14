import factory
from template.tests.factories.action_factory import ActionFactory
from .area_factory import AreaFactory
from .patient_factory import PatientFactory
from game.models import ActionInstance, ActionInstanceState, ActionInstanceStateNames


class ActionInstanceStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstanceState
        django_get_or_create = (
            "action_instance",
            "name",
            "t_local_begin",
            "t_local_end",
        )

    action_instance = factory.SubFactory("game.tests.factories.ActionInstanceFactory")
    name = ActionInstanceStateNames.PLANNED
    t_local_begin = 0
    t_local_end = None


class FailedActionInstanceStateFactory(ActionInstanceStateFactory):
    name = ActionInstanceStateNames.DECLINED
    info_text = "Missing so much stuff, what were you thinking?"


class ActionInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstance
        django_get_or_create = ("patient", "area", "action_instance", "current_state")

    patient = factory.SubFactory(PatientFactory)
    area = factory.SubFactory(AreaFactory)
    action_instance = factory.SubFactory(ActionFactory)
    current_state = factory.SubFactory(ActionInstanceStateFactory)
