# Generated by Django 5.0.1 on 2024-06-20 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0007_material_is_lab_alter_material_category"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="patientinformation",
            name="consecutive_unique_number",
        ),
    ]
