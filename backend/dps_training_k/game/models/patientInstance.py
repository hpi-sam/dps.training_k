from django.db import models


class PatientInstance(models.Model):
    name = models.CharField(
        max_length=100
    )  # technically default patient but kept here for simplicity for now
    # patientID = models.ForeignKey()  # currently called "SensenID"
    # exerciseID = models.ForeignKey()
    # stateID = models.ForeignKey()
    # measureID = models.ManyToManyField()
    isLoggedIn = models.BooleanField()
    patientCode = models.IntegerField(
        help_text="patientCode used to log into patient - therefore part of authentication"
    )

    def __str__(self):
        return f"Patient #{self.id} called {self.name} with code {self.patientCode}"
