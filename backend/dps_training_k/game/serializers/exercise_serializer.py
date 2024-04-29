from rest_framework import serializers

import game.models.area as a
import game.models.exercise as e
import game.models.patient_instance as pt
import game.models.personnel as p

"""Serializers for the sending the exercise event. All Serializers except for ExerciseSerializers are just helpers"""


class PatientInstanceSerializer(serializers.ModelSerializer):
    patientId = serializers.IntegerField(source="patient_frontend_id", read_only=True)
    patientName = serializers.CharField(source="name", read_only=True)
    code = serializers.IntegerField(source="static_information.code", read_only=True)

    class Meta:
        model = pt.PatientInstance
        fields = ["patientId", "patientName", "code", "triage"]


class PersonnelSerializer(serializers.ModelSerializer):
    personnelId = serializers.IntegerField(source="pk", read_only=True)
    personnelName = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = p.Personnel
        fields = ["personnelId", "personnelName"]


class AreaSerializer(serializers.ModelSerializer):
    areaName = serializers.CharField(source="name", read_only=True)
    patients = PatientInstanceSerializer(
        source="patientinstance_set", many=True, read_only=True
    )
    personnel = PersonnelSerializer(source="personnel_set", many=True, read_only=True)
    material = serializers.SerializerMethodField()  # TODO: implement material

    class Meta:
        model = a.Area
        fields = ["areaName", "patients", "personnel", "material"]

    def get_material(self, obj):
        return []  # Return an empty list for material until it's implemented


class ExerciseSerializer(serializers.ModelSerializer):
    exerciseId = serializers.CharField(source="exercise_frontend_id", read_only=True)
    areas = AreaSerializer(source="area_set", many=True, read_only=True)

    class Meta:
        model = e.Exercise
        fields = ["exerciseId", "areas"]
