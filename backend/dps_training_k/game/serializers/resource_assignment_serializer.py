from django.db.models import Q
from rest_framework import serializers

from game.models import Personnel, MaterialInstance, Area


class PersonnelResourceSerializer(serializers.ModelSerializer):
    personnelId = serializers.IntegerField(source="id")
    patientId = serializers.SerializerMethodField()

    class Meta:
        model = Personnel
        fields = ["personnelId", "patientId"]

    @staticmethod
    def get_patientId(obj):
        return obj.patient_instance.frontend_id if obj.patient_instance else None


class MaterialInstanceResourceSerializer(serializers.ModelSerializer):
    materialId = serializers.IntegerField(source="id")
    patientId = serializers.SerializerMethodField()

    class Meta:
        model = MaterialInstance
        fields = ["materialId", "patientId"]

    @staticmethod
    def get_patientId(obj):
        return obj.patient_instance.frontend_id if obj.patient_instance else None


class AreaResourceSerializer(serializers.ModelSerializer):
    personnel = serializers.SerializerMethodField(method_name="get_personnel")
    material = serializers.SerializerMethodField(method_name="get_material")
    areaId = serializers.IntegerField(source="id")

    class Meta:
        model = Area
        fields = ["areaId", "personnel", "material"]

    @staticmethod
    def get_personnel(obj):
        personnel_qs = Personnel.objects.filter(
            Q(patient_instance__area=obj) | Q(area=obj)
        )
        return PersonnelResourceSerializer(personnel_qs, many=True).data

    @staticmethod
    def get_material(obj):
        material_qs = MaterialInstance.objects.filter(
            Q(patient_instance__area=obj) | Q(area=obj)
        )
        return MaterialInstanceResourceSerializer(material_qs, many=True).data
