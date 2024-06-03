from rest_framework import serializers
import game.models.action_instance as ai
import game.models.scheduled_event as se


class PatientRelocatingSerializer(serializers.ModelSerializer):
    relocatingInfo = serializers.SerializerMethodField()
    timeUntilBack = serializers.SerializerMethodField()

    class Meta:
        model = ai.ActionInstance
        fields = ["relocatingInfo", "timeUntilBack"]
        read_only = fields

    def get_relocatingInfo(self, action_instance):
        return f"{action_instance.name} wird gerade ausgeführt"

    def get_timeUntilBack(self, action_instance):
        return se.ScheduledEvent.get_time_until_completion(action_instance)
