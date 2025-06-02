import json
from common import ENCODING

def encode_message(action: str, data: dict) -> bytes:
    msg = {"action" : action,
           "data"   : data 
           }
    return json.dumps(msg).encode(ENCODING)

def decode_message(raw: bytes) -> str:
    return json.loads(raw.decode(ENCODING))