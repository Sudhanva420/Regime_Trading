import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import numpy as np
import ta


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
    'target_vol': 0.02,
    'vol_window': 50
}

'''
self.I() will call the fucntion that you pass in
Expects that function to return a precomputed NumPy array or pandas Series 
'''


def compute_returns(close):
     
    close = pd.Series(close)
    returns =  close.pct_change()
    return returns.to_numpy() #We cant return series back to self(I)

 
class MyStrategy3(Strategy):

    def init(self):
        
        self.sma = self.I(lambda: self.data.df['ema_200'], name='ema_200')
        self.momentum = self.I(lambda: self.data.df['momentum'], name='momentum')
        self.rsi = self.I(lambda: self.data.df['RSI'], name='RSI')
        self.regime = self.I(lambda: self.data.df['regime'], name='regime')
        self.returns = self.I(compute_returns, self.data.Close)
        self.target_vol = 0.1


#Position_Size = (target_vol/current_vol)

    
    
    def next(self):
        
        if self.regime[-1] == 1:
            if self.momentum[-1] > CONFIG["momentum_threshold"]:
                if not self.position:
                    
                    if np.isnan(self.returns[-1]):
                        return 
                    
                    lookback_window = CONFIG["vol_window"]
                    recent_returns = self.returns[-lookback_window:]

                    if np.isnan(recent_returns).any():
                        return

                    actual_vol = np.std(recent_returns)
                    if actual_vol == 0:
                        return
                    
                    pos_size = self.target_vol/actual_vol
                    while np.isnan(pos_size):
                        return 
                    
                    pos_size = int(pos_size)
                    
                    if pos_size>0:
                        self.buy(size = pos_size)
            else:
                self.position.close()
                
        elif self.regime[-1] == 0:
            
            if self.rsi[-1] <= CONFIG["rsi_entry"]:
                if not self.position:
                    
                    if np.isnan(self.returns[-1]):
                        return 
                    
                    lookback_window = CONFIG["vol_window"]
                    recent_returns = self.returns[-lookback_window:]

                    if np.isnan(recent_returns).any():
                        return
                    
                    actual_vol = np.std(recent_returns)
                    if actual_vol == 0:
                        return
                    
                    pos_size = self.target_vol/actual_vol
                    while np.isnan(pos_size):
                        return
                    
                    pos_size = int(pos_size)
                    
                    if pos_size>0:
                        self.buy(size = pos_size)
                        
            elif self.rsi[-1] >= 70:
                self.position.close()


from backtesting import Backtest

bt = Backtest(df, MyStrategy3, cash=10_000, commission=.002)
stats = bt.run()
print(stats)
        