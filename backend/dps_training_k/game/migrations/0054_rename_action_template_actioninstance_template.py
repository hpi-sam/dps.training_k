# Generated by Django 5.0.1 on 2024-05-16 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0053_personnel_is_blocked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='actioninstance',
            old_name='action_template',
            new_name='template',
        ),
    ]
