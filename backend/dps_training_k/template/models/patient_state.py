from django.db import models


class PatientState(models.Model):
    # this field might be deleted. It only serves the purpose of being able to query patients by their sensenID. This is could be outsourced to a seperate table as well
    # stateID = models.IntegerField(
    #    help_text="state number as it is used in original data set"
    # )
    # the foreign key of patient might be enough. Thus this field might be deleted. The only benefit of this field is to be able to query related states from a patient object in a simple way
    # patients = models.ManyToManyField("game.Patient", related_name="states")
    transition = models.ForeignKey(
        "StateTransition", on_delete=models.CASCADE, null=True, blank=True
    )
    data = models.JSONField(help_text="data for patient in current phase")
    state_phase = models.IntegerField()
    is_dead = models.BooleanField(default=False)

    def is_final(self):
        return self.transition.resulting_state is None

    # class Meta:
    #    unique_together = (
    #        "stateID",
    #        "patientID",
    #    )
