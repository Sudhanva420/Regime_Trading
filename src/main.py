import pandas as pd

from backtesting import Backtest
from signal_generation import Signal
from strategy_4_2 import MyStrategy2
from visualization import Plots

if __name__ == "__main__":
    
    df = pd.read_csv("/Users/sudhanvabharadwaj/Desktop/Interview_Practice/Regime_Momentum/Data/shop.csv")
    
    df = Signal.make_signals(df)

    df.to_csv("signals_with_regime.csv", index=False)

    #print(df.tail())
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    
    bt = Backtest(df, MyStrategy2, cash=10_000, commission=.002)
    stats = bt.run()
    print(stats)
    
    strategy_instance = bt.strategy
    equity_over_time = strategy_instance.portfolio_value
    
    portfolio_series = pd.DataFrame(
    strategy_instance.portfolio_value,
    index=strategy_instance.data.df.index[-len(strategy_instance.portfolio_value):],
    columns=["Portfolio Value"]
    )
    
    Plots.equity_curve(portfolio_series)
    
    #bt.plot()
    
    
    
   

    
    
    