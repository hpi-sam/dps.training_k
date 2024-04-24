from django.db import models


class Triage(models.TextChoices):
    UNDEFINED = "-", "undefined"
    RED = "R", "red"
    YELLOW = "Y", "yellow"
    GREEN = "G", "green"
    Airway = "A", "airway"
    BREATHING = "B", "breathing"
    CIRCULATION = "C", "circulation"
    DISABILITY = "D", "disability"
    EXPOSURE = "E", "exposure"
