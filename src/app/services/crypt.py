import base64
import json


def base64_encode(data: dict) -> str:
    """Encodes a dictionary as a base64 string."""
    json_data = json.dumps(data)
    return base64.b64encode(json_data.encode()).decode()
