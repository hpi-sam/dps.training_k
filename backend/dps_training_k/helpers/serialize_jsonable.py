from django.core.serializers.json import DjangoJSONEncoder
import json


class SerializeJSONAble:
    def to_json(self):
        return json.dumps(self, cls=DjangoJSONEncoder)
