import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np

df = pd.read_csv("/Users/sudhanvabharadwaj/Desktop/Interview_Practice/Regime_Momentum/Data/regime_signals.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')

#print(df.index)

CONFIG = {
    'momentum_lookback': 100,
    'momentum_threshold': 0.05,
    'rsi_period': 14,
    'rsi_entry': 30,
    'rsi_exit': 50,
    'rebalancing_freq': 'W',  
    'stop_loss_pct': 0.05,
    'vol_window': 20,
    'target_vol': 0.02
}


class MyStrategy(Strategy):
    
    def init(self):
        self.sma = self.I(lambda: self.data.df['ema_200'], name='ema_200')
        self.momentum = self.I(lambda: self.data.df['momentum'], name='momentum')
        self.rsi = self.I(lambda: self.data.df['RSI'], name='RSI')
        self.regime = self.I(lambda: self.data.df['regime'], name='regime')

    def next(self):
        
        if self.regime[-1] == 1:
            if self.momentum[-1] > CONFIG["momentum_threshold"]:
                if not self.position:
                    self.buy()
            else:
                self.position.close()
                
        elif self.regime[-1] == 0:
            if self.rsi[-1] <= CONFIG["rsi_entry"]:
                if not self.position:
                    self.buy()
            elif self.rsi[-1] >= 70:
                self.position.close()

from backtesting import Backtest

bt = Backtest(df, MyStrategy, cash=10_000, commission=.002)
stats = bt.run()
print(stats)
        