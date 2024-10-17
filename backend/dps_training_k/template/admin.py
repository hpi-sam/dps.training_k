from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Action)
admin.site.register(PatientState)
admin.site.register(StateTransition)
admin.site.register(PatientInformation)
admin.site.register(Material)
admin.site.register(ContinuousVariable)
