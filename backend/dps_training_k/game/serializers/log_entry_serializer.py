import pytz
from rest_framework import serializers

import game.models.log_entry as le
import game.models.personnel as pe


class LogEntrySerializer(serializers.ModelSerializer):
    logId = serializers.IntegerField(source="local_id")
    logMessage = serializers.CharField(source="message")
    logTime = serializers.SerializerMethodField()
    areaId = serializers.SerializerMethodField()
    patientId = serializers.SerializerMethodField()
    personnelIds = serializers.PrimaryKeyRelatedField(
        source="personnel",
        queryset=pe.Personnel.objects.all(),
        many=True,
        allow_null=True,
    )
    materialNames = serializers.SerializerMethodField()

    class Meta:
        model = le.LogEntry
        fields = [
            "logId",
            "logMessage",
            "logTime",
            "areaId",
            "patientId",
            "personnelIds",
            "materialNames",
        ]
        read_only_fields = fields

    def get_logTime(self, obj):
        # Ensure the timestamp is timezone aware
        timestamp = obj.timestamp.replace(tzinfo=pytz.UTC)
        return int(timestamp.timestamp() * 1000)

    def get_areaId(self, obj):
        return obj.area.pk if obj.area else None

    def get_patientId(self, obj):
        return obj.patient_instance.frontend_id if obj.patient_instance else None

    def get_materialNames(self, obj):
        return [material.name for material in obj.materials.all()]
