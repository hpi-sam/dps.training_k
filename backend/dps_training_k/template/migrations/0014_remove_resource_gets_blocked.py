# Generated by Django 5.0.1 on 2024-04-24 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0013_resource'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='gets_blocked',
        ),
    ]
