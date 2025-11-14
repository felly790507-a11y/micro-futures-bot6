# micro-futures-bot6
micro-futures-bot6
專案架構概覽
本專案同時支援 v3 規則型 與 v4 回歸型 的微期交易系統，並提供完整的回測、視覺化、最佳化與走勢分段校正工具鏈。

目錄結構
engines/

DecisionEngine.py → v3 規則型：bias、score_entry、score_exit、should_enter

DecisionEngine_v2.py → v4 回歸型：evaluate_tick → bias、bias_prob、entry_score_v2、exit_score_v2

StrategyState.py → 持倉管理與風控：stoploss/takeprofit/exit_score/tick/time

TickEngine.py → 主循環：整合 v3/v4 引擎、指標、記錄

io/

TradeLogger.py → 交易事件記錄

TickRecorder.py → tick 記錄

TradeAnalyzer.py → 回測分析彙總

models/

ParamsStore.py → 權重版本管理 JSON

RegressionCalibrator.py → 分段權重校正，寫入 ParamsStore

backtest/

BacktestDataLoader.py → K 線轉 tick

BacktestRunner.py → 回測執行

ResultVisualizer.py → 盈虧曲線、勝率分布、版本比較

PerformanceReporter.py → Sharpe、最大回撤、平均持倉時間

WalkforwardTester.py → 分段校正 + 回測

Optimizer.py → 多參數最佳化

ReportExporter.py → CSV/Markdown 匯出

config/

strategy_config.json → risk/decision 參數集合

ConfigManager.py → 載入配置

pipeline/

polars_indicator_utils.py → 以 Polars 產生指標

root

KlineInitializer.py → 資料準備

StrategyLoop.py → 線上策略迴圈；可參考 TickEngine 結構

main.py → 入口

模組引用關係
TickEngine

inputs: tick dict（含 price、volume、timestamp 和指標）

uses: DecisionEngine_v2（v4）或 DecisionEngine（v3）、StrategyState、IndicatorEngine.extract_features、MultiTimeframeEngine、TradeLogger、TickRecorder、ParamsStore

outputs: 交易事件、tick 記錄、狀態更新

BacktestRunner

inputs: ticks（list[dict]）

orchestrates: TickEngine → TradeAnalyzer

outputs: 分析結果（dict）、trade_log.csv、tick_data.csv

WalkforwardTester

split → calibrate → run → analyze → version manage

Optimizer

param_grid → run combinations → find best metric

Config contracts
decision

entry_threshold: float

exit_threshold: float

bias_prob_threshold: float

risk

stoploss_atr_mult: float

takeprofit_atr_mult: float

max_ticks: int

max_minutes: int

Data contracts
tick dict

required: price, volume, timestamp

common indicators: rsi, macd, macd_signal, macd_hist, ema5, ema20, adx, atr, vwap, bband_pos, is_ready, is_ready_5m, is_ready_15m

v4 fields (computed): bias, bias_prob, entry_score_v2, exit_score_v2, params_version, mode

Quick start
準備資料

使用 KlineInitializer.py 或 BacktestDataLoader.py 將 K 線轉成 ticks。

跑回測

BacktestRunner(mode="regression_based" | "rule_based").run(ticks)

視覺化與報告

ResultVisualizer("trade_log.csv").plot_pnl_curve()

PerformanceReporter("trade_log.csv").report()

ReportExporter().export_csv([...]); export_markdown([...])

走勢分段校正

WalkforwardTester(params_path, config_path).run_walkforward(ticks, segment_size=500)

參數最佳化

Optimizer(ticks).find_best(param_grid, mode="regression_based", metric="avg_pnl")
