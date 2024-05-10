import factory
from template.tests.factories.action_factory import (
    ActionFactory,
    ActionFactoryWithEffectDuration,
)
from .area_factory import AreaFactory
from .patient_factory import PatientFactory
from game.models import ActionInstance, ActionInstanceState, ActionInstanceStateNames
from django.db.models import Max


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


class ActionInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
            "order_id",
        )

    patient_instance = None
    area = None
    lab = None
    action_template = factory.SubFactory(ActionFactory)
    current_state = None
    # gets maximum order id for the associated patient_instance, then adds 1
    # or sets to 1 if no order_id was found for this patient_instance
    order_id = factory.LazyAttribute(
        lambda o: (
            ActionInstance.objects.filter(
                patient_instance=o.patient_instance
            ).aggregate(Max("order_id"))["order_id__max"]
            or 0
        )
        + 1
    )

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = ActionInstanceStateFactory(action_instance=self)


class ActionInstanceFactoryWithEffectDuration(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
        )

    patient_instance = None
    area = None
    lab = None
    action_template = factory.SubFactory(ActionFactoryWithEffectDuration)
    current_state = None

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = ActionInstanceStateFactory(action_instance=self)
