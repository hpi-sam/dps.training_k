from rest_framework import serializers
from template.models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["name", "category", "is_returnable"]
