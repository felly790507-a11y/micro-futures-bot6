import csv
import os
from datetime import datetime

class TickRecorder:
    def __init__(self, filename="tick_record.csv", max_ticks=5):
        self.filename = filename
        self.max_ticks = max_ticks
        self.records = []
        self.current_trade_id = None
        self.tick_buffer = []

        # 初始化檔案
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "trade_id", "timestamp", "tick_index",
                    "price", "volume", "vwap", "momentum", "direction_score"
                ])

    def start_trade(self, trade_id: str):
        self.current_trade_id = trade_id
        self.tick_buffer = []

    def record_tick(self, tick: dict):
        if self.current_trade_id is None:
            return

        tick_data = {
            "trade_id": self.current_trade_id,
            "timestamp": tick.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "tick_index": len(self.tick_buffer),
            "price": tick.get("close", 0),
            "volume": tick.get("volume", 0),
            "vwap": tick.get("vwap", 0),
            "momentum": tick.get("momentum", 0),
            "direction_score": tick.get("direction_score", 0)
        }

        self.tick_buffer.append(tick_data)

        if len(self.tick_buffer) >= self.max_ticks:
            self.auto_flush()

    def auto_flush(self):
        self._write_to_file()
        self.reset()

    def force_flush(self):
        if self.tick_buffer:
            self._write_to_file()
        self.reset()

    def _write_to_file(self):
        with open(self.filename, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "trade_id", "timestamp", "tick_index",
                "price", "volume", "vwap", "momentum", "direction_score"
            ])
            writer.writerows(self.tick_buffer)

    def reset(self):
        self.tick_buffer = []
        self.current_trade_id = None
