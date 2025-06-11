from utils.event_scope import cli_dispatcher
from utils.events import (
    GameEvent, GameWonEvent, GameDrawEvent, MovePlacedEvent, InvalidMoveEvent)
from utils.log_utils import GameLogger

logger = GameLogger

@cli_dispatcher.register(GameWonEvent)
def log_win(event: GameEvent):
    logger.log_result("win")

@cli_dispatcher.register(GameDrawEvent)
def log_draw(event: GameEvent):
    logger.log_result("draw")

@cli_dispatcher.register(MovePlacedEvent)
def log_move(event: MovePlacedEvent):
    logger.log_step(
        player_name = event.player.name,
        player_id = event.player.id,
        symbol = event.player.symbol,
        x = event.x,
        y = event.y,
        board_state = event.board.get_state()  
    ) 

@cli_dispatcher.register(MovePlacedEvent)
def handle_move(event):
    print(f"{event.player.name} placed at ({event.x}, {event.y})")

@cli_dispatcher.register(GameWonEvent)
def handle_win(event):
    print(f"{event.winner.name} wins!")

@cli_dispatcher.register(GameDrawEvent)
def handle_draw(event):
    print("It's a draw!")

@cli_dispatcher.register(InvalidMoveEvent)
def handle_invalid(_):
    print("Invalid move.")