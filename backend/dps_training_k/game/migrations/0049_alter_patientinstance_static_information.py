# Generated by Django 5.0.1 on 2024-05-13 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0048_merge_20240513_1910'),
        ('template', '0016_alter_action_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientinstance',
            name='static_information',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='template.patientinformation'),
        ),
    ]
