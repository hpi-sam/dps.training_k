from rest_framework import serializers
import game.models.log_entry as le
import game.models.patient_instance as pa

import game.models.lab as la
import game.models.personnel as pe
from datetime import datetime
import pytz


class LogEntrySerializer(serializers.ModelSerializer):
    logId = serializers.IntegerField(source="local_id")
    logMessage = serializers.CharField(source="message")
    logTime = serializers.SerializerMethodField()
    areaName = serializers.SerializerMethodField()
    patientId = serializers.PrimaryKeyRelatedField(
        source="patient_instance",
        queryset=pa.PatientInstance.objects.all(),
        allow_null=True,
    )
    labId = serializers.PrimaryKeyRelatedField(
        source="lab", queryset=la.Lab.objects.all(), allow_null=True
    )
    personnelIds = serializers.PrimaryKeyRelatedField(
        source="personnel",
        queryset=pe.Personnel.objects.all(),
        many=True,
        allow_null=True,
    )

    class Meta:
        model = le.LogEntry
        fields = [
            "logId",
            "logMessage",
            "logTime",
            "areaName",
            "patientId",
            "labId",
            "personnelIds",
        ]
        read_only_fields = fields

    def get_logTime(self, obj):
        # Ensure the timestamp is timezone aware
        timestamp = obj.timestamp.replace(tzinfo=pytz.UTC)
        return int(timestamp.timestamp() * 1000)

    def get_areaName(self, obj):
        return obj.area.name if obj.area else None
