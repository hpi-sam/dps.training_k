from django.contrib import admin
from .models import Exercise, SavedExercise

# Register your models here.
admin.site.register(Exercise)
admin.site.register(SavedExercise)
