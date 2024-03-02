from helpers.invitation_logic import LevenshteinCode
import datetime

CODE_LENGTH = 6
INVITATION_LOGIC = LevenshteinCode(CODE_LENGTH)
CURRENT_SECONDS = datetime.datetime.now().timestamp
