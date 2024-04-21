import factory
from template.models import StateTransition


class StateTransitionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StateTransition

    next_state_transition = None
    resulting_state = None
