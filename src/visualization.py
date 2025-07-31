# plot_equity_curve(stats), plot_rolling_sharpe(), etc.

import matplotlib.pyplot as plt
import seaborn as sns

class Plots:
    
    @staticmethod
    def equity_curve(data):
        
        
        plt.figure(figsize=(12,10))
        plt.xlabel('Time')
        plt.ylabel('Portfolio Value')
        
        plt.plot(data.index, data['Portfolio_Value'])
        plt.grid(True)
        
        plt.show()
    
    