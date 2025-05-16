import socket
from common import HOST, PORT, BUFFER_SIZE, ENCODING
from protocol import encode_message, decode_message

# create socket object to listen for TCP connections.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Binding IPs and Ports
s.bind((HOST, PORT))

# Start listening, waiting for client connection
s.listen()
print("Waiting for players' connectinon")

# receive one client connection
clientsocket,addr = s.accept()      
print("Connected by Address: %s" % str(addr))


while True:

    # receive data
    data = clientsocket.recv(BUFFER_SIZE)

    # If empty data, disconnect
    if not data:
        break 
   
    # decode the message from client
    msg = decode_message(data)
    print(f"Received: {msg}")

    # if action is move, print it out
    if msg["action"] == "move":
        x = msg["data"]["x"]
        y = msg["data"]["y"]
        print(f"The position({x}, {y})")
    
    # reply status to client
    reply = {"status" : "ok",
             "next" : "player2"
            }
    clientsocket.send(encode_message("update", reply))
    
# close connection
clientsocket.close()
