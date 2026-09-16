import json
from network.common import ENCODING

class ConnectionClosedError(Exception):
    """Raised when the remote peer closes the TCP connection."""
    pass

def encode_message(action: str, data: dict) -> bytes:
    msg = {"action" : action,
        "data"   : data 
        }
    return json.dumps(msg).encode(ENCODING)

def decode_message(raw: bytes) -> dict:
    if not raw:
        raise ConnectionClosedError("Remote peer closed the connection.")
    return json.loads(raw.decode(ENCODING))