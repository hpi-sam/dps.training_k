from rest_framework import serializers
from template.models import Material


class MaterialSerializer(serializers.ModelSerializer):
    materialName = serializers.CharField(source="name")
    materialType = serializers.CharField(source="category")

    class Meta:
        model = Material
        fields = ["materialName", "materialType"]
        read_only = fields
