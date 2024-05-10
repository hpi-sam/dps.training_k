from rest_framework import serializers
import game.models.log_entry as le
from datetime import datetime
import pytz


class LogEntrySerializer(serializers.ModelSerializer):
    logId = serializers.IntegerField(source="local_id")
    logMessage = serializers.CharField(source="message")
    logTime = serializers.SerializerMethodField()
    areaName = serializers.CharField(source="area.name")
    patientId = serializers.IntegerField(source="patient_instance.id")
    labId = serializers.IntegerField(source="lab.id")
    personnelId = serializers.IntegerField(source="personnel.id")

    class Meta:
        model = le.LogEntry
        fields = [
            "logId",
            "logMessage",
            "logTime",
            "areaName",
            "patientId",
            "labId",
            "personnelId",
        ]
        read_only_fields = fields

    def get_logTime(self, obj):
        # Ensure the timestamp is timezone aware
        timestamp = obj.timestamp.replace(tzinfo=pytz.UTC)
        return int(timestamp.timestamp() * 1000)
