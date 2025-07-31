Regime-Switching Momentum Strategy with Dynamic Position Sizing

This project implements a robust regime-aware trading strategy that dynamically switches between momentum and mean-reversion logic. It includes dynamic position sizing based on volatility and extensive backtesting analysis using Python.

---

## Strategy Overview

The strategy detects **market regimes** using a 200-day EMA:
- **Bullish Regime**: Apply momentum strategy.
- **Bearish Regime**: Apply RSI-based mean-reversion strategy.

### Features:
- Regime switching logic using trend filters
- Dynamic position sizing:
  - ATR-based scaling
  - Target volatility-based scaling
- Stop-loss mechanism
- Rolling Sharpe ratio, drawdown, and underwater equity curve
- Modular, reusable codebase with clear structure

