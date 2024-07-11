import factory

from helpers.triage import Triage
from template.models import PatientInformation
from template.constants import ActionIDs


class PatientInformationFactory(factory.django.DjangoModelFactory):
    """Equivalent to the Patient number 1004"""

    class Meta:
        model = PatientInformation
        django_get_or_create = ("code",)

    code = 1004
    personal_details = "Helena Raedder 15.03.1964 Albert-Einstein-Str. 34, 06122 Halle"
    blood_type = 1
    injury = "ca. 8 cm große, weit klaffende Kopfplatzwunde re. temporal, blutet noch; im Wundgrund vermutlich Knochensplitter sichtbar."
    biometrics = "weiblich; ca. 52; blond, braune Augen, Brille, 1,82 m"
    triage = (Triage.GREEN,)
    consecutive_unique_number = 5225
    mobility = "initial gehfähig"
    preexisting_illnesses = "funktionelle Herzbeschwerden; beginnender Bechterew"
    permanent_medication = "Schlafmittel"
    current_case_history = (
        "wird vom Rettungsdienst gebracht: habe eine Deckenplatte vor den Kopf bekommen; "
        "Verband durchgeblutet; nicht bewusstlos gewesen."
    )
    pretreatment = "Wundversorgung,"
    pretreatment_action_templates = {str(ActionIDs.WUNDVERSORGUNG): 1}
