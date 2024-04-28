from rest_framework import serializers
from template.models import Resource
from helpers.serialize_jsonable import SerializeJSONAble


class ResourceSerializer(SerializeJSONAble, serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["name", "category", "is_returnable"]
