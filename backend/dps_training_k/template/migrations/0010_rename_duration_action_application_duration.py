# Generated by Django 5.0.1 on 2024-04-14 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0009_alter_action_category_alter_action_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='action',
            old_name='duration',
            new_name='application_duration',
        ),
    ]
