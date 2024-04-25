from django.utils import timezone

from helpers.id_generator import LevenshteinCode

CODE_LENGTH = 6
ID_GENERATOR = LevenshteinCode(CODE_LENGTH)
CURRENT_TIME = lambda: timezone.now()
DEFAULT_STATE_ID = 101
