import socket
from network.common import HOST, PORT, BUFFER_SIZE
from network.protocol import encode_message, decode_message
from gameLogic.online_game import OnlineGame
from gameLogic.player import Player, Human_Player
from utils.log_utils import GameLogger
from typing import List

LOG_FILE = "game_log.txt"

def log(message: str):
    with open(LOG_FILE, "a", encoding = "utf-8") as f:
        f.write(message + "\n")


# create list for multiple players
clients: list[socket.socket] = []
addresses: list[socket.AddressInfo] = []

# setup for the online game and players
game = OnlineGame()

players:List[Player] = []

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
        msg = decode_message(conn.recv(BUFFER_SIZE))
        players.append(Human_Player(len(clients), msg['data']['name'],msg['data']['symbol'] ))
        conn.send(encode_message("player id", {"id" : len(clients)}))
        print(f"Player {len(clients)} connection : {addr}")
    

def run_game():
    turn = 0
    log("\n=== New Game Start ===")
    while True:
        current = clients[turn]
        other = clients[(turn + 1) % 2]
        current_player_id = turn
        player = players[turn]

        # told player that what they need to do now
        other.send(encode_message("wait", {}))

        # receive the place from the player current y
        current.send(encode_message("your_turn", {}))
        msg = decode_message(current.recv(BUFFER_SIZE))
        x, y = msg["data"]["x"], msg["data"]["y"]

        result = game.place_and_check(current_player_id, x, y)
        while result == "invalid":
            current.send(encode_message("your_turn(re)", {}))
            msg = decode_message(current.recv(BUFFER_SIZE))
            x, y = msg["data"]["x"], msg["data"]["y"]
            result = game.place_and_check(current_player_id, x, y)
        log(f"Player {player.id} ({player.symbol}) placed at ({x}, {y})")
        for c in clients:
            c.send(encode_message("update", {"board": game.get_board_str()}))            

        if result == "win":
            winner = game.get_winner()
            for c in clients:
                c.send(encode_message("result", {"winner": winner}))
            log(f"Player {winner} ({player.symbol}) wins!")
        elif result == "draw":
            for c in clients:
                c.send(encode_message("result", {"winner": None}))
            log(f"Game ends in a draw.")
        else:
            turn = (turn + 1) % 2
            continue

        msg = decode_message(current.recv(BUFFER_SIZE))
        if msg["action"] == "restart":
            game.restart()
            log("Game restarted by player request.")
            turn = 0
        else:
            break

    print("Game ended.")
    for c in clients:
        c.close()
        # symbol = players[turn].symbol
        # turn_count += 1
        # log(f"Turn {turn_count}: Player {players[turn].id} ({symbol}) placed at ({x}, {y})")
        # # check win or draw
        # if game.check_win(turn, x, y):
        #     log(f"Winner: Player {players[turn].id} ({players[turn].symbol})")
        #     for c in clients:
        #         c.send(encode_message("result", {"winner": players[turn].id}))
        #     if decode_message(current.recv(BUFFER_SIZE))["action"] == "restart":
        #         game.restart_game()
        #         turn = 0  # start from Player 1 
        #         turn_count = 0
        #         log("=== Game End ===\n")
        #         continue
        #     else: break
        # elif game.check_draw():
        #     log("Result: Draw")
        #     for c in clients:
        #         c.send(encode_message("result", {"winner": None}))
        #     if decode_message(current.recv(BUFFER_SIZE))["action"] == "restart":
        #         game.restart_game()
        #         turn = 0  # start from Player 1 
        #         turn_count = 0
        #         log("=== Game End ===\n")
        #         continue
        #     else: break

        # board = game.board
        # for c in clients:
        #     c.send(encode_message("update", {"board": str(board)}))

        # turn = (turn + 1) %2

if __name__ == "__main__":
    wait_for_players()
    run_game()