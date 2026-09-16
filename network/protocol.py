import json
import socket
from network.common import ENCODING
HEADER_LEN = 4

class ConnectionClosedError(Exception):
    """Raised when the remote peer closes the TCP connection."""
    pass

def encode_message(action: str, data: dict) -> bytes:
    msg = {"action" : action,
        "data"  : data 
    }

    payload = json.dumps(msg).encode(ENCODING)
    header = len(payload).to_bytes(HEADER_LEN, byteorder="big")
    return header + payload

def recv_exact(sock:socket.socket, num_bytes: int) -> bytes:
    received = b''
    while len(received) < num_bytes:
        remaining = num_bytes - len(received)
        chunk = sock.recv(remaining)
        if not chunk:
            raise ConnectionClosedError(f"Connection closed while receiving message: \
                                        Expected: {num_bytes} bytes, received {len(received)}")
        else:
            received += chunk
    return received

def receive_message(sock:socket.socket) -> dict:
    header = recv_exact(sock, HEADER_LEN)
    num_bytes = int.from_bytes(header, byteorder="big")
    msg = recv_exact(sock, num_bytes)

    return json.loads(msg.decode(ENCODING))