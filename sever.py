import socket
import threading 
from common import HOST, PORT, BUFFER_SIZE
from protocol import encode_message, decode_message
from online_game import OnlineGame
import player

LOG_FILE = "game_log.txt"

def log(message: str):
    with open(LOG_FILE) as f:
        f.write(message + "\n")


# create list for multiple players
clients: list[socket.socket] = []
addresses: list[socket.AddressInfo] = []

# setup for the online game and players
game = OnlineGame()

players = [
    player.Human_Player(1, "Player1", "X"),
    player.Human_Player(2, "Player2", "O")
]

game.set_players(players)


def wait_for_players():
    print("Waiting for two players' connection ")
    # create socket object to listen for TCP connections.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding IPs and Ports
    s.bind((HOST, PORT))

    # Start listening, waiting for client connection
    s.listen()

    while len(clients) < 2:
        conn, addr = s.accept()
        clients.append(conn)
        addresses.append(addr)
        conn.send(encode_message("player id", {"id" : len(clients)}))
        print(f"Player {len(clients)} connection : {addr}")
    

def run_game():
    turn = 0
    log("\n=== New Game Start ===")
    turn_count = 0
    while True:
        current = clients[turn]
        other = clients[(turn + 1) % 2]

        # told player that what they need to do now
        other.send(encode_message("wait", {}))

        # receive the place from the player current y
        current.send(encode_message("your_turn", {}))
        msg = decode_message(current.recv(BUFFER_SIZE))
        x, y = msg["data"]["x"], msg["data"]["y"]
        while not game.place_piece(turn, x, y):
            current.send(encode_message("your_turn(re)", {}))
            msg = decode_message(current.recv(BUFFER_SIZE))
            x, y = msg["data"]["x"], msg["data"]["y"]

        symbol = players[turn].symbol
        turn_count += 1
        log(f"Turn {turn_count}: Player {players[turn].id} ({symbol}) placed at ({x}, {y})")
        # check win or draw
        if game.check_win(turn, x, y):
            log(f"Winner: Player {players[turn].id} ({players[turn].symbol})")
            for c in clients:
                c.send(encode_message("result", {"winner": players[turn].id}))
            if decode_message(current.recv(BUFFER_SIZE))["action"] == "restart":
                game.restart_game()
                turn = 0  # start from Player 1 
                turn_count = 0
                log("=== Game End ===\n")
                continue
            else: break
        elif game.check_draw():
            log("Result: Draw")
            for c in clients:
                c.send(encode_message("result", {"winner": None}))
            if decode_message(current.recv(BUFFER_SIZE))["action"] == "restart":
                game.restart_game()
                turn = 0  # start from Player 1 
                turn_count = 0
                log("=== Game End ===\n")
                continue
            else: break

        board = game.board
        for c in clients:
            c.send(encode_message("update", {"board": str(board)}))

        turn = (turn + 1) %2

if __name__ == "__main__":
    wait_for_players()
    run_game()