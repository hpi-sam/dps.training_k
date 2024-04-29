from rest_framework import serializers

import game.models.area as a
import game.models.exercise as e
import game.models.patient_instance as pt
import game.models.personnel as p

"""Serializers for the sending the exercise event. All Serializers except for ExerciseSerializers are just helpers"""


class PatientInstanceSerializer(serializers.ModelSerializer):
    patientId = serializers.IntegerField(source="patient_frontend_id")
    patientName = serializers.CharField(source="name")
    code = serializers.IntegerField(source="static_information.code")

    class Meta:
        model = pt.PatientInstance
        fields = ["patientId", "patientName", "code", "triage"]
        read_only = ["patientId", "patientName", "code", "triage"]


class PersonnelSerializer(serializers.ModelSerializer):
    personnelId = serializers.IntegerField(source="pk")
    personnelName = serializers.CharField(source="name")

    class Meta:
        model = p.Personnel
        fields = ["personnelId", "personnelName"]
        read_only = ["personnelId", "personnelName"]


class AreaSerializer(serializers.ModelSerializer):
    areaName = serializers.CharField(source="name")
    patients = PatientInstanceSerializer(source="patientinstance_set", many=True)
    personnel = PersonnelSerializer(source="personnel_set", many=True)
    material = serializers.SerializerMethodField()  # TODO: implement material

    class Meta:
        model = a.Area
        fields = ["areaName", "patients", "personnel", "material"]
        read_only = ["areaName", "patients", "personnel", "material"]

    def get_material(self, obj):
        return []  # Return an empty list for material until it's implemented


class ExerciseSerializer(serializers.ModelSerializer):
    exerciseId = serializers.CharField(source="exercise_frontend_id")
    areas = AreaSerializer(source="area_set", many=True)

    class Meta:
        model = e.Exercise
        fields = ["exerciseId", "areas"]
        read_only = ["exerciseId", "areas"]
