from django.contrib import admin
from .models import *
from template.models import *

# Register your models here.
admin.site.register(Exercise)
admin.site.register(SavedExercise)
admin.site.register(Area)
admin.site.register(Patient)
admin.site.register(Personnel)
admin.site.register(ScheduledEvent)
