import socket
from common import HOST, PORT, BUFFER_SIZE, ENCODING

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Connection Successfully")
msg = s.recv(1024)
print(msg.decode(ENCODING))
s.close()