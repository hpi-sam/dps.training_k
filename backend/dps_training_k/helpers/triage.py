from django.db import models


class Triage(models.TextChoices):
    UNDEFINED = "-", "Gray"
    BLACK = "X", "Black"
    RED = "1", "Red"
    YELLOW = "2", "Yellow"
    GREEN = "3", "Green"
