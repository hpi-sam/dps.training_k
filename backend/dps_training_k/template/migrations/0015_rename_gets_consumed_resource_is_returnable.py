# Generated by Django 5.0.1 on 2024-04-24 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0014_remove_resource_gets_blocked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='gets_consumed',
            new_name='is_returnable',
        ),
    ]
