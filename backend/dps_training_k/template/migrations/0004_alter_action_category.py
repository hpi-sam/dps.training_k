# Generated by Django 5.0.1 on 2024-05-30 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0003_action_location_alter_action_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="category",
            field=models.CharField(
                choices=[
                    ("TR", "treatment"),
                    ("EX", "examination"),
                    ("PR", "production"),
                    ("IM", "imaging"),
                    ("OT", "other"),
                ],
                max_length=2,
            ),
        ),
    ]
