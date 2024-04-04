# Generated by Django 5.0.1 on 2024-04-04 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0002_alter_patientstate_unique_together_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StateTransition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "next_state_transition",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="template.statetransition",
                    ),
                ),
                (
                    "resulting_state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="template.patientstate",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="patientstate",
            name="transition",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="template.statetransition",
            ),
        ),
    ]
