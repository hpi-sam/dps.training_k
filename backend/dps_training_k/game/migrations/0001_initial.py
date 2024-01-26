# Generated by Django 5.0.1 on 2024-01-24 14:32

import django.db.models.deletion
import helpers.invitation_logic
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SavedExercise",
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
                ("savedExercise", models.JSONField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
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
                    "invitation_code",
                    models.CharField(
                        default=helpers.invitation_logic.LevenshteinCode.get_invitation_code,
                        editable=False,
                        max_length=6,
                        unique=True,
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("C", "configuration"),
                            ("R", "running"),
                            ("P", "paused"),
                            ("F", "finished"),
                        ],
                        default="C",
                    ),
                ),
                (
                    "config",
                    models.ForeignKey(
                        default='{\n    "glossary": {\n        "title": "example glossary",\n\t\t"GlossDiv": {\n            "title": "S",\n\t\t\t"GlossList": {\n                "GlossEntry": {\n                    "ID": "SGML",\n\t\t\t\t\t"SortAs": "SGML",\n\t\t\t\t\t"GlossTerm": "Standard Generalized Markup Language",\n\t\t\t\t\t"Acronym": "SGML",\n\t\t\t\t\t"Abbrev": "ISO 8879:1986",\n\t\t\t\t\t"GlossDef": {\n                        "para": "A meta-markup language, used to create markup languages such as DocBook.",\n\t\t\t\t\t\t"GlossSeeAlso": ["GML", "XML"]\n                    },\n\t\t\t\t\t"GlossSee": "markup"\n                }\n            }\n        }\n    }\n}',
                        on_delete=django.db.models.deletion.CASCADE,
                        to="game.savedexercise",
                    ),
                ),
            ],
        ),
    ]
