# Generated by Django 5.0.1 on 2024-04-18 15:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0011_action_effect_duration_action_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientstate',
            name='transition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='template.statetransition'),
        ),
    ]
