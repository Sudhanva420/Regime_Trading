#Python file to take in a dataframe and give out a dataframe with all the required signals and regimes within

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import talib

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

class Signal:
    
    @staticmethod
    def make_signals(df):
        
        df['ema_200'] = df['Close'].rolling(window=200).mean()
        
        df['momentum'] = (df['Close'] / df["Close"].shift(CONFIG["momentum_lookback"])) - 1
        
        df['RSI'] = talib.RSI(df['Close'], timeperiod = CONFIG["rsi_period"])
        
        df["regime"] = np.where(df['Close'] > df['ema_200'],1,0)
        
        return df
    
    
    