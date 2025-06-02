import json
import os
from datetime import datetime
from typing import List

TRACE_DIR = '../logs'
TRACE_INDEX_FILE = os.path.join(TRACE_DIR, "trace_index.txt")

os.makedirs(TRACE_DIR, exist_ok=True)


class GameLogger:

    def __init__(self):
        self.trace: List[dict] = []
        self.trace_id = self._get_next_trace_id()

    
    def _get_next_trace_id(self) -> int:
        # ## get all the 
        # existing = [f for f in os.listdir(TRACE_DIR) if f.startswith("trace_") and f.endswith(".json")]
        # nums = [int(f[6:9]) for f in existing if f[6:9].isdigit()]
        # return max(nums, default=0) + 1
        if not os.path.exists(TRACE_INDEX_FILE):
            with open(TRACE_INDEX_FILE, "w") as f:
                f.write("1\n")
            return 1
        
        with open(TRACE_INDEX_FILE, "r+") as f:
            new_id = int(f.readline().strip()) + 1
            f.seek(0)
            f.write(str(new_id) + "\n")
            f.close()
            return new_id
    
    def log_step(self, player_name: str, player_id: int, symbol: str, x: int, y: int, board_state: List[List[str]]):
        """_summary_

        Args:
            player_name (str): _description_
            player_id (int): _description_
            x (int): _description_
            y (int): _description_
            board_state (List[List[str]]): _description_
        """
        self.trace.append({
            "timestamp" : datetime.now().isoformat(),
           "player_id": player_id,
            "player_name": player_name,
            "symbol": symbol,
            "move": [x, y],
            "board": board_state,
            "result": None
        })

    def log_result(self, result: str):
            if self.trace:
                self.trace[-1]["result"] = result

    def save_trace(self):
        filename = f"trace_{self.trace_id:04d}.json"
        path = os.path.join(TRACE_DIR, filename)
        with open(path, "w") as f:
            json.dump(self.trace, f, indent=2)
        print(f"Trace saved to {path}")


 
