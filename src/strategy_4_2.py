import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np
import ta


#df = pd.read_csv("/Users/sudhanvabharadwaj/Desktop/Interview_Practice/Regime_Momentum/Data/regime_signals.csv")
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
    'target_vol': 0.02,
    'stop_multiplier': 2
}

#from backtesting.lib import ATR
from ta.volatility import AverageTrueRange

def compute_atr(high, low, close, window):
    
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)

    atr_series = AverageTrueRange(high=high, low=low, close=close, window=window).average_true_range()
    return atr_series.values  # convert to NumPy array for use in self.I
    
'''
self.I() will call the fucntion that you pass in
Expects that function to return a precomputed NumPy array or pandas Series 
'''
class MyStrategy2(Strategy):

    def init(self):
        
        self.sma = self.I(lambda: self.data.df['ema_200'], name='ema_200')
        self.momentum = self.I(lambda: self.data.df['momentum'], name='momentum')
        self.rsi = self.I(lambda: self.data.df['RSI'], name='RSI')
        self.regime = self.I(lambda: self.data.df['regime'], name='regime')
        self.entry_price = None
        
        self.atr = self.I(
            compute_atr,
            self.data.High,
            self.data.Low,
            self.data.Close,
            14
        ) #ATR = Average True Range, this is used to dynamically change the size of positions based on volatilitty

        self.portfolio_value = []
    def trailing_stoploss(self):
        
        self.__stop_value = 2*(compute_atr(self.data.High, self.data.Low, self.data.Close, 14))
        
#Position_Size = (risk_per_trade * equity) / (ATR * multiplier)

    def next(self):
        
        self.portfolio_value.append(self.equity)
        
        risk_per_trade = 0.05
        multiplier = 1.5
        slippage = 0.1
        transaction_cost = 0.2
        target_profit = .1
        
        if self.position:
            
            if (self.data.Close[-1]/self.entry_price) - 1 > target_profit:
                self.entry_price= None
                self.position.close()
        
        if self.regime[-1] == 1:
            
            if self.momentum[-1] > CONFIG["momentum_threshold"]:
                if not self.position:
                    
                    if np.isnan(self.atr[-1]) or self.atr[-1]==0:
                        return  # waiting for non nan atr
                    
                    stop_loss = self.data.Close[-1] - self.atr[-1]*CONFIG['stop_multiplier']
                    pos_size = (risk_per_trade*self.equity)/(self.atr[-1]*multiplier)
                    pos_size = int(pos_size)
                    
                    if pos_size>0:
                        self.buy(size = pos_size, sl = stop_loss)
                        self.entry_price = self.data.Close[-1]
                        
            elif self.position:
                self.position.close()

                
        elif self.regime[-1] == 0:
            
            if self.rsi[-1] <= CONFIG["rsi_entry"]:
                if not self.position:
                    
                    if np.isnan(self.atr[-1]) or self.atr[-1]==0:
                        return  # waiting for non nan atr
                    
                    stop_loss = self.data.Close[-1] - self.atr[-1]*CONFIG['stop_multiplier']
                    pos_size = (risk_per_trade*self.equity)/(self.atr[-1]*multiplier)
                    pos_size = int(pos_size)
                    
                    if pos_size>0:
                        self.buy(size = pos_size, sl = stop_loss)
                        self.entry_price = self.data.Close[-1]
                        
            elif self.rsi[-1] >= 70:
                if self.position:
                    self.position.close()

'''
from backtesting import Backtest

bt = Backtest(df, MyStrategy2, cash=10_000, commission=.002)
stats = bt.run()
print(stats)

bt.plot()
'''