import base64
import json


def encode_dict_to_base64(data: dict) -> str:
    return base64.b64encode(json.dumps(data).encode()).decode()


def encode_str_to_base64(string: str) -> str:
    return base64.b64encode(string.encode()).decode()


def decode_json_data_from_base64(base64_string: str) -> dict:
    return json.loads(base64.b64decode(base64_string).decode())


