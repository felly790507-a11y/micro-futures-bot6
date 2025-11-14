from datetime import datetime
import time

from KlineInitializer import KlineInitializer
from StrategyState import StrategyState
from TickEngine import TickEngine

class StrategyLoop:
    def __init__(self, api=None, contract=None, simulation=True):
        self.api = api
        self.contract = contract
        self.simulation = simulation

        self.kline = KlineInitializer()
        self.state = StrategyState()
        self.tick_engine = None

    def initialize(self):
        print("[INIT] 抓取 K 線與指標中...")
        self.kline.fetch_kline()
        self.kline.compute_indicators()
        bias = self.kline.get_market_bias()
        print(f"[BIAS] 市場偏向：{bias}")

        self.tick_engine = TickEngine(self.state, bias, self.kline.indicators)

    def simulate_ticks(self):
        print("[SIM] 模擬 Tick 資料流中...")
        ticks = [
            {"price": 27300, "volume": 20, "bid": 27299, "ask": 27301, "timestamp": datetime.now(), "rsi": 60},
            {"price": 27290, "volume": 18, "bid": 27289, "ask": 27291, "timestamp": datetime.now(), "rsi": 58},
            {"price": 27270, "volume": 22, "bid": 27269, "ask": 27271, "timestamp": datetime.now(), "rsi": 55},
            {"price": 27240, "volume": 25, "bid": 27239, "ask": 27241, "timestamp": datetime.now(), "rsi": 52},
            {"price": 27210, "volume": 30, "bid": 27209, "ask": 27211, "timestamp": datetime.now(), "rsi": 50}
        ]

        for tick in ticks:
            self.tick_engine.on_tick(tick)
            time.sleep(1)

    def run(self):
        self.initialize()

        if self.simulation:
            self.simulate_ticks()
        else:
            print("🚀 等待 Tick 觸發策略中...")
