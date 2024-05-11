import django.db.models.deletion
from django.core.management import call_command
from django.db import migrations, models


def populate_patient_instance_static_information_relation(apps, schema_editor):
    PatientInstance = apps.get_model("game", "PatientInstance")
    PatientInformation = apps.get_model("template", "PatientInformation")

    if not PatientInstance.objects.filter(static_information__isnull=True).exists():
        return

    call_command("patient_information")

    patient_information = PatientInformation.objects.get(code=1004)

    for patient_instance in PatientInstance.objects.filter(static_information=None):
        patient_instance.static_information = patient_information
        patient_instance.save()


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0042_actioninstance_one_or_more_field_not_null_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="patientinstance",
            name="static_information",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="template.patientinformation",
            ),
        ),
        migrations.RunPython(populate_patient_instance_static_information_relation),
    ]
