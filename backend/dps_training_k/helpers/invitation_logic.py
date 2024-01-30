import string
import random
from Levenshtein import distance as lev


class LevenshteinCode:
    def __init__(self, code_length):
        self.code_length = code_length
        self.codes_taken = []

    def get_invitation_code(self):
        """
        Generates an unique alphabetic invitation_code of length self.code_length,
        that is also distinctive from other non-finished excercises (levenshtein distance >= 3).
        :return: a string, the invitation_code
        """
        new_code = None
        letters = string.ascii_lowercase
        while not new_code:
            new_code = "".join(random.choice(letters) for _ in range(self.code_length))
            for code_taken in self.codes_taken:
                if (
                    lev(str(code_taken), str(new_code)) < 3
                ):  # should be different at minimum 3 places
                    new_code = None
        self.codes_taken.append(new_code)
        return new_code
