import socket
import sys
from common import HOST, PORT, BUFFER_SIZE, ENCODING

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

s.listen()

print("Waiting for players' connectinon")

while True:
    # 建立客户端连接
    clientsocket,addr = s.accept()      

    print("Address: %s" % str(addr))
   
    msg='Welcome to sever！'+ "\r\n"
    clientsocket.send(msg.encode(ENCODING))
    clientsocket.close()
