# Generated by Django 5.0.1 on 2024-04-18 12:45

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0010_rename_duration_action_application_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='effect_duration',
            field=models.IntegerField(default=None, help_text='Effect duration in seconds in realtime. Might be scaled by external factors.', null=True),
        ),
        migrations.AddField(
            model_name='action',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
