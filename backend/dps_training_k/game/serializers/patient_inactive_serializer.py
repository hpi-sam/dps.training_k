from rest_framework import serializers
import game.models.action_instance as ai
import game.models.scheduled_event as se


class PatientInactiveSerializer(serializers.ModelSerializer):
    inactiveInfo = serializers.SerializerMethodField()
    timeUntilBack = serializers.SerializerMethodField()

    class Meta:
        model = ai.ActionInstance
        fields = ["inactiveInfo", "timeUntilBack"]
        read_only = fields

    def get_inactiveInfo(self, imaging_instance):
        return f"{imaging_instance.name} wird gerade ausgeführt"

    def get_timeUntilBack(self, imaging_instance):
        return se.ScheduledEvent.get_time_until_completion(imaging_instance)
