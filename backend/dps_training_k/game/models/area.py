from django.db import models


class Area(models.Model):
    name = models.CharField(unique=True, max_length=30)
    exerciseId = models.ForeignKey("Exercise", on_delete=models.CASCADE)
    isPaused = models.BooleanField()
    # labID = models.ForeignKey("Lab")

    @classmethod
    def create_area(cls, name, exercise, isPaused = False):
        unique_name = name
        number = 1

        # Loop until a unique name is found
        while cls.objects.filter(name=unique_name).exists():
            unique_name = f"{name}{number}"
            number += 1
        
        return cls.objects.create(name=unique_name, exerciseId=exercise, isPaused=isPaused)