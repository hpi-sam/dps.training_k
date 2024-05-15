# Generated by Django 5.0.1 on 2024-05-10 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_merge_20240503_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='personnel',
            name='action_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.actioninstance'),
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.IntegerField(blank=True)),
                ('timestamp', models.DateTimeField(blank=True, help_text='May only be set while exercise is running', null=True)),
                ('message', models.TextField()),
                ('is_dirty', models.BooleanField(default=False, help_text='Set to True if log_entry is missing Keys (e.g. personnel)')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.area')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.exercise')),
                ('patient_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.patientinstance')),
                ('personnel', models.ManyToManyField(blank=True, to='game.personnel')),
            ],
        ),
        migrations.AddConstraint(
            model_name='logentry',
            constraint=models.UniqueConstraint(fields=('local_id', 'exercise'), name='unique_local_id_for_entry'),
        ),
    ]
