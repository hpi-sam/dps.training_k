from django.db.models import Q
from rest_framework import serializers

import game.models.area as a
import game.models.exercise as e
import game.models.material_instance as m
import game.models.patient_instance as pt
import game.models.personnel as p

"""Serializers for the sending the exercise event. All Serializers except for ExerciseSerializers are just helpers"""


class PatientInstanceSerializer(serializers.ModelSerializer):
    patientId = serializers.CharField(source="frontend_id")
    patientName = serializers.CharField(source="name")
    code = serializers.IntegerField(source="patient_template.info.code")

    class Meta:
        model = pt.PatientInstance
        fields = ["patientId", "patientName", "code", "triage"]
        read_only = fields


class PersonnelSerializer(serializers.ModelSerializer):
    personnelId = serializers.IntegerField(source="id")
    personnelName = serializers.CharField(source="name")

    class Meta:
        model = p.Personnel
        fields = ["personnelId", "personnelName"]
        read_only = fields


class MaterialInstanceSerializer(serializers.ModelSerializer):
    materialId = serializers.IntegerField(source="id")
    materialType = serializers.CharField(source="template.category")
    materialName = serializers.CharField(source="template.name")

    class Meta:
        model = m.MaterialInstance
        fields = [
            "materialId",
            "materialType",
            "materialName",
        ]
        read_only = fields


class AreaSerializer(serializers.ModelSerializer):
    @staticmethod
    def get_material(obj):
        material = m.MaterialInstance.objects.filter(
            Q(area=obj) | Q(patient_instance__area=obj)
        )
        return MaterialInstanceSerializer(material, many=True).data

    @staticmethod
    def get_personnel(obj):
        personnel = p.Personnel.objects.filter(
            Q(area=obj) | Q(patient_instance__area=obj)
        )
        return PersonnelSerializer(personnel, many=True).data

    areaId = serializers.IntegerField(source="id")
    areaName = serializers.CharField(source="name")
    patients = PatientInstanceSerializer(source="patientinstance_set", many=True)
    personnel = serializers.SerializerMethodField(method_name="get_personnel")
    material = serializers.SerializerMethodField(method_name="get_material")

    class Meta:
        model = a.Area
        fields = ["areaId", "areaName", "patients", "personnel", "material"]
        read_only = fields


class ExerciseSerializer(serializers.ModelSerializer):
    exerciseId = serializers.CharField(source="frontend_id")
    areas = AreaSerializer(source="area_set", many=True)

    class Meta:
        model = e.Exercise
        fields = ["exerciseId", "areas"]
        read_only = fields
