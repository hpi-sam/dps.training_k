from rest_framework import serializers
import game.models.log_entry as le
import game.models.patient_instance as pa

# import game.models.lab as la ToDo: Uncomment once lab is on main
import game.models.personnel as pe
from datetime import datetime
import pytz


class LogEntrySerializer(serializers.ModelSerializer):
    logId = serializers.IntegerField(source="local_id")
    logMessage = serializers.CharField(source="message")
    logTime = serializers.SerializerMethodField()
    areaName = serializers.CharField(source="area.name")
    patientId = serializers.PrimaryKeyRelatedField(
        queryset=pa.PatientInstance.objects.all()
    )
    # labId = serializers.PrimaryKeyRelatedField(queryset=la.Lab.objects.all())
    personnelIds = serializers.PrimaryKeyRelatedField(
        queryset=pe.Personnel.objects.all(), many=True
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
            "personnelId",
        ]
        read_only_fields = fields

    def get_logTime(self, obj):
        # Ensure the timestamp is timezone aware
        timestamp = obj.timestamp.replace(tzinfo=pytz.UTC)
        return int(timestamp.timestamp() * 1000)
