import json
from typing import Any


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if not isinstance(obj, (int, float, bool)):
            return str(obj)
        return super().default(obj)
