import factory
from template.tests.factories.action_factory import (
    ActionFactory,
    ActionFactoryWithEffectDuration,
)
from .area_factory import AreaFactory
from .patient_factory import PatientFactory
from .lab_factory import LabFactory
from game.models import (
    PatientActionInstance,
    LabActionInstance,
    ActionInstanceState,
    ActionInstanceStateNames,
)


class ActionInstanceStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstanceState
        django_get_or_create = (
            "patient_action_instance",
            "lab_action_instance",
            "t_local_begin",
            "t_local_end",
        )

    patient_action_instance = factory.SubFactory(
        "game.tests.factories.PatientActionInstanceFactory"
    )
    lab_action_instance = None
    name = ActionInstanceStateNames.PLANNED
    t_local_begin = 0
    t_local_end = None


class PatientActionInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
        )

    patient_instance = factory.SubFactory(PatientFactory)
    area = factory.SubFactory(AreaFactory)
    lab = None
    action_template = factory.SubFactory(ActionFactory)
    current_state = None

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = ActionInstanceStateFactory(patient_action_instance=self)


class FailedActionInstanceStateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ActionInstanceState
        django_get_or_create = (
            "patient_action_instance",
            "lab_action_instance",
            "name",
            "t_local_begin",
            "t_local_end",
        )

    patient_action_instance = factory.SubFactory(
        "game.tests.factories.PatientActionInstanceFactory"
    )
    lab_action_instance = None
    name = ActionInstanceStateNames.DECLINED
    t_local_begin = 0
    t_local_end = None
    info_text = "Test text regarding missing some ressources and this not being part of a work queue"


class ActionInstanceFactoryFailedState(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
        )

    patient_instance = factory.SubFactory(PatientFactory)
    area = factory.SubFactory(AreaFactory)
    lab = None
    action_template = factory.SubFactory(ActionFactory)
    current_state = None

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = FailedActionInstanceStateFactory(
            patient_action_instance=self
        )


class ActionInstanceFactoryWithEffectDuration(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
        )

    patient_instance = factory.SubFactory(PatientFactory)
    area = factory.SubFactory(AreaFactory)
    lab = None
    action_template = factory.SubFactory(ActionFactoryWithEffectDuration)
    current_state = None

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = ActionInstanceStateFactory(patient_action_instance=self)


class LabActionInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = LabActionInstance
        django_get_or_create = (
            "patient_instance",
            "area",
            "lab",
            "action_template",
            "current_state",
        )

    patient_instance = None
    area = None
    lab = factory.SubFactory(LabFactory)
    action_template = factory.SubFactory(ActionFactory)
    current_state = None

    @factory.post_generation
    def set_current_state(self, create, extracted, **kwargs):
        if not create:
            return
        self.current_state = ActionInstanceStateFactory(lab_action_instance=self)
