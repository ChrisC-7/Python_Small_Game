import socket
from common import HOST, PORT, BUFFER_SIZE, ENCODING
from protocol import encode_message, decode_message

# create socket object, based on TCP agreement
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the sever
s.connect((HOST, PORT))
print("Connection Successfully")


# enter the loop, get the piece placement by user's input x, y
while True:
    x = int(input("Input row (x): "))
    y = int(input("Input col (y): "))

    # send the placement's info as networking message
    s.send(encode_message("move", {"x": x, "y": y}))

    # receive the response from sever(update or comformation)
    response = decode_message(s.recv(BUFFER_SIZE))
    print("From server:", response)

# close the connection
s.close()
