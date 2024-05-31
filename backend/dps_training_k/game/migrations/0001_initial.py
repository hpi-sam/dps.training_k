# Generated by Django 5.0.1 on 2024-05-27 15:00

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import game.models.patient_instance
import helpers.eventable
import helpers.local_timable
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('template', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isPaused', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frontend_id', models.CharField(unique=True)),
                ('state', models.CharField(choices=[('C', 'configuration'), ('R', 'running'), ('P', 'paused'), ('F', 'finished')], default='C')),
            ],
            bases=(helpers.eventable.NonEventable, models.Model),
        ),
        migrations.CreateModel(
            name='SavedExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True)),
                ('saved_exercise', models.JSONField()),
                ('time_speed_up', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('P', 'Patient'), ('T', 'Trainer')], default='P', max_length=1)),
                ('channel_name', models.CharField(blank=True, max_length=100, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ActionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(null=True)),
                ('historic_patient_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='template.patientstate')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='template.action')),
            ],
            options={
                'ordering': ['order_id'],
            },
            bases=(helpers.local_timable.LocalTimeable, models.Model),
        ),
        migrations.CreateModel(
            name='ActionInstanceState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('PL', 'planned'), ('IP', 'in_progress'), ('OH', 'on_hold'), ('FI', 'finished'), ('IE', 'in effect'), ('EX', 'expired'), ('CA', 'canceled')], max_length=2)),
                ('t_local_begin', models.IntegerField()),
                ('t_local_end', models.IntegerField(blank=True, null=True)),
                ('info_text', models.CharField(blank=True, default=None, null=True)),
                ('action_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='game.actioninstance')),
            ],
        ),
        migrations.AddField(
            model_name='actioninstance',
            name='current_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.actioninstancestate'),
        ),
        migrations.AddField(
            model_name='actioninstance',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='game.area'),
        ),
        migrations.AddField(
            model_name='area',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.exercise'),
        ),
        migrations.CreateModel(
            name='Lab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.exercise')),
            ],
        ),
        migrations.AddField(
            model_name='actioninstance',
            name='lab',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.lab'),
        ),
        migrations.CreateModel(
            name='PatientInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Max Mustermann', max_length=100)),
                ('frontend_id', models.CharField(help_text='patient_frontend_id used to log into patient - see validator for format', max_length=6, unique=True, validators=[game.models.patient_instance.validate_patient_frontend_id])),
                ('triage', models.CharField(choices=[('-', 'Gray'), ('X', 'Black'), ('1', 'Red'), ('2', 'Yellow'), ('3', 'Green')], default='-')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.area')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.exercise')),
                ('patient_state', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='template.patientstate')),
                ('static_information', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='template.patientinformation')),
                ('user', models.OneToOneField(blank=True, help_text='User object for authentication - has to be deleted explicitly or manually', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            bases=(helpers.eventable.Eventable, models.Model),
        ),
        migrations.CreateModel(
            name='MaterialInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.actioninstance')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.area')),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.lab')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='template.material')),
                ('patient_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.patientinstance')),
            ],
        ),
        migrations.AddField(
            model_name='actioninstance',
            name='patient_instance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.patientinstance'),
        ),
        migrations.CreateModel(
            name='Personnel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('action_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='game.actioninstance')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.area')),
                ('lab', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.lab')),
                ('patient_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.patientinstance')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_id', models.IntegerField(blank=True)),
                ('timestamp', models.DateTimeField(blank=True, help_text='May only be set while exercise is running', null=True)),
                ('message', models.TextField()),
                ('is_dirty', models.BooleanField(default=False, help_text='Set to True if objects is missing relevant Keys (e.g. timestamp)')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.area')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.exercise')),
                ('materials', models.ManyToManyField(blank=True, to='game.materialinstance')),
                ('patient_instance', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.patientinstance')),
                ('personnel', models.ManyToManyField(blank=True, to='game.personnel')),
            ],
        ),
        migrations.AddField(
            model_name='exercise',
            name='config',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='game.savedexercise'),
        ),
        migrations.CreateModel(
            name='ScheduledEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateTimeField()),
                ('kwargs', models.TextField(blank=True, null=True)),
                ('method_name', models.CharField(max_length=100)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='game.exercise')),
            ],
            options={
                'ordering': ['exercise', 'end_date'],
            },
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_instance_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to='game.actioninstance')),
                ('area_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to='game.area')),
                ('exercise_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to='game.exercise')),
                ('patient_owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_events', to='game.patientinstance')),
                ('event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='game.scheduledevent')),
            ],
        ),
        migrations.AddConstraint(
            model_name='area',
            constraint=models.UniqueConstraint(fields=('name', 'exercise'), name='unique_area_names_per_exercise'),
        ),
        migrations.AddConstraint(
            model_name='materialinstance',
            constraint=models.CheckConstraint(check=models.Q(('lab__isnull', False), ('patient_instance__isnull', False), ('area__isnull', False), _connector='OR'), name='one_or_more_field_not_null_material'),
        ),
        migrations.AddConstraint(
            model_name='actioninstance',
            constraint=models.UniqueConstraint(fields=('order_id', 'patient_instance'), name='unique_order_id_for_patient'),
        ),
        migrations.AddConstraint(
            model_name='actioninstance',
            constraint=models.CheckConstraint(check=models.Q(('lab__isnull', False), ('patient_instance__isnull', False), _connector='OR'), name='one_or_more_field_not_null_action'),
        ),
        migrations.AddConstraint(
            model_name='logentry',
            constraint=models.UniqueConstraint(fields=('local_id', 'exercise'), name='unique_local_id_for_entry'),
        ),
        migrations.AddConstraint(
            model_name='owner',
            constraint=models.CheckConstraint(check=models.Q(('action_instance_owner__isnull', False), ('patient_owner__isnull', False), ('exercise_owner__isnull', False), ('area_owner__isnull', False), _connector='OR'), name='one_or_more_field_not_null_owner'),
        ),
    ]
