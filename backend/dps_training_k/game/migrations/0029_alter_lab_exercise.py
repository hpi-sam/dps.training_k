# Generated by Django 5.0.1 on 2024-04-25 16:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0028_alter_inventory_area_lab_inventory_lab_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lab',
            name='exercise',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.exercise'),
        ),
    ]
