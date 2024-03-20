from helpers.invitation_logic import LevenshteinCode
from django.utils import timezone

CODE_LENGTH = 6
INVITATION_LOGIC = LevenshteinCode(CODE_LENGTH)
CURRENT_TIME = lambda: timezone.now()
