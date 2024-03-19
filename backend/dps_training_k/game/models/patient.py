from django.db import models


class Patient(models.Model):
    name = models.CharField(
        max_length=100, default="Max Mustermann"
    )  # technically patientData but kept here for simplicity for now
    # patientCode = models.ForeignKey()  # currently called "SensenID"
    exercise = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    # stateID = models.ForeignKey()
    # measureID = models.ManyToManyField()
    patientId = models.IntegerField(
        help_text="patientId used to log into patient - therefore part of authentication"
    )

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with ID {self.patientId}"
