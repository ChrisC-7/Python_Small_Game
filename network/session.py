from network.common import BUFFER_SIZE
from network.protocol import encode_message,decode_message
from gameLogic.player import AIPlayer, Human_Player, Player
from gameLogic.online_game import OnlineGame
from utils.log_utils import GameLogger
from utils.events import InvalidMoveEvent, GameWonEvent, GameDrawEvent
from typing import List
import socket

class PlayerConnection:
    def __init__(self, player: Player, socket:socket.socket, address):
        self.player = player
        self.socket = socket
        self.address = address
        self.active = True
        
    def send(self, action: str, data: dict = {}):
        msg = encode_message(action, data)
        print(f"[Server -> {self.address}] Sending: {msg}")
        self.socket.send(msg)
    
    def receive(self) -> dict:
        return decode_message(self.socket.recv(BUFFER_SIZE))

    def close(self):
        self.socket.close()        

class OnlineGameSession:
    def __init__(self):
        self.connections: List[PlayerConnection] = []
        self.turn = 0
        self.game = OnlineGame()
        self.logger = GameLogger()
        self.game.engine.logger = self.logger

    def accept_players(self, server_socket:socket.socket):
        print("Waiting for 2 players to connect...")
        while len(self.connections) < 2:
            conn, addr = server_socket.accept()
            


            intro_msg = decode_message(conn.recv(BUFFER_SIZE))
            name = intro_msg["data"]["name"]
            symbol = intro_msg["data"]["symbol"]
            player = Human_Player(len(self.connections), name, symbol)
            conn.send(encode_message("player id", {"id": len(self.connections)}))
            self.connections.append(PlayerConnection(player, conn, addr))
            print(f"Player {len(self.connections)} connected from {addr}")
    
        players = [pc.player for pc in self.connections]
        self.game.set_players(players)

    def run_game_loop(self):
        print("\n===Game Start===")
        while True:
            current = self.connections[self.turn]
            opponent = self.connections[(self.turn + 1) % 2 ]
            player = current.player

            opponent.send("wait")
            current.send("your_turn")
            print(f"[DEBUG] Sending your_turn to Player {player.id}")

            move_msg = current.receive()
            if move_msg["action"] == "disconnect":
                break
            
            x, y = move_msg["data"]["x"], move_msg["data"]["y"]
            event = self.game.engine.place_piece(x, y)

            while isinstance(event, InvalidMoveEvent):
                current.send("your_turn(re)", {})
                move_msg = current.receive()
                if move_msg["action"] == "disconnect":
                    break
                x, y = move_msg["data"]["x"], move_msg["data"]["y"]
                event = self.game.engine.place_piece(x, y)

            
            self.boardcast("update", {"board": self.game.get_board_str()})

            
            if isinstance(event, GameWonEvent):
                winner_id = player.id
                for conn in self.connections:
                    conn.send("result", {"winner": winner_id})
                print(f"[Result] Player {player.name} wins.")
                self.logger.log_result("win")
            elif isinstance(event, GameDrawEvent):
                for conn in self.connections:
                    conn.send("result", {"winner": None})
                print("[Result] Game ends in a draw.")
                self.logger.log_result("draw")
            else:
                self.turn = (self.turn + 1) % 2
                continue

            # check if restart
            # restart_msg = current.receive()
            # if restart_msg["action"] == "restart":
            #     self.game.restart()
            #     self.logger = GameLogger()
            #     self.game.engine.logger = self.logger
            #     self.turn = 0
            #     print("[Restart] Game restarted.")
            # else:
            #     break
            restart_votes = []

            for conn in self.connections:
                msg = conn.receive()
                if msg["action"] == "restart":
                    restart_votes.append(True)
                else:
                    restart_votes.append(False)

            if all(restart_votes):
                print("[Server] Both players agreed to restart.")
                self.game.restart()
                self.logger = GameLogger()
                self.game.engine.logger = self.logger
                self.turn = 0
                print("[Restart] Game restarted.")
            else:
                print("[Server] One or both players declined restart. Ending game.")
                break

        for conn in self.connections:
            conn.close()
        print("Game ended. All connections closed.")

    def boardcast(self, action: str, data: dict):
        for conn in self.connections:
            conn.send(action, data)

    