# Generated by Django 5.0.1 on 2024-05-03 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0030_alter_inventory_area_alter_inventory_lab_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='inventory',
            name='one_or_more_field_not_null_inventory',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='area',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='lab',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='patient_instance',
        ),
        migrations.AddField(
            model_name='area',
            name='inventory',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.inventory'),
        ),
        migrations.AddField(
            model_name='lab',
            name='inventory',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.inventory'),
        ),
        migrations.AddField(
            model_name='patientinstance',
            name='inventory',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.inventory'),
        ),
    ]
