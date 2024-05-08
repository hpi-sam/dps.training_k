from rest_framework import serializers
from template.models import Action


class ActionSerializer(serializers.ModelSerializer):
    actionName = serializers.CharField(source="name")
    actionCategory = serializers.CharField(source="category")

    class Meta:
        model = Action
        fields = ["actionName", "actionCategory"]
        read_only = fields
