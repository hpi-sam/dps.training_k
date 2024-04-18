import factory
from template.models import StateTransition


class StateTransitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StateTransition
        django_get_or_create = ("next_state_transition", "resulting_state")

    next_state_transition = None
    resulting_state = None
