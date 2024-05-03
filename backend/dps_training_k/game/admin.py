from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Exercise)
admin.site.register(SavedExercise)
admin.site.register(Area)
admin.site.register(PatientInstance)
admin.site.register(Personnel)
admin.site.register(ScheduledEvent)
admin.site.register(PatientActionInstance)
admin.site.register(LabActionInstance)
admin.site.register(ActionInstanceState)
admin.site.register(User)
