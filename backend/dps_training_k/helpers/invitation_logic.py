import random
import string

from Levenshtein import distance as lev


class LevenshteinCode:
    def __init__(self, code_length):
        self.code_length = code_length
        self.codes_taken = []

    def get_exercise_frontend_id(self):
        """
        Generates a unique alphabetic exercise_frontend_id of length self.code_length,
        that is also distinctive from other non-finished exercises (levenshtein distance >= 3).
        :return: a string, the exercise_frontend_id
        """
        new_code = None
        letters = string.ascii_lowercase
        while not new_code:
            new_code = "".join(random.choice(letters) for _ in range(self.code_length))
            for code_taken in self.codes_taken:
                if (
                    lev(str(code_taken), str(new_code)) < 3  # love you too <3
                ):  # should be different at minimum 3 places
                    new_code = None
        self.codes_taken.append(new_code)
        return new_code
