import socket
from common import HOST, PORT, BUFFER_SIZE, ENCODING
from protocol import encode_message, decode_message
import board

def get_numeric_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a valid number.")

# create socket object, based on TCP agreement
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the sever
s.connect((HOST, PORT))

msg = decode_message(s.recv(BUFFER_SIZE))
player_id = msg["data"]["id"]


# enter the loop, get the piece placement by user's input x, y
while True:
    msg = decode_message(s.recv(BUFFER_SIZE))
    action = msg["action"]
    data = msg["data"]
    if action == "your_turn" :
        print("It's your turn now! ")
        x = get_numeric_input("Input row (x): ")
        y = get_numeric_input("Input col (y): ")
        # send the placement's info as networking message
        s.send(encode_message("move", {"x": x, "y": y}))
    elif action == "your_turn(re)" :
        print("Your input is not valid, please re-enter")
        x = get_numeric_input("Input row (x): ")
        y = get_numeric_input("Input col (y): ")
        # send the placement's info as networking message
        s.send(encode_message("move", {"x": x, "y": y}))
    elif action == "wait":
        print("Sorry it's not your turn, please wait")
    elif action == "result":
        if data["winner"] == None:
            print("It's draw")
        elif data["winner"] == player_id:
            print("Congradulations! You win")
        else:
            print("Sorry, You lose")
        
        choice = input("Play again? (y/n): ")
        if choice.lower() == 'y':
            s.send(encode_message("restart", {}))
        else: break
    elif action == "update":
        print(data["board"])



# close the connection
s.close()
