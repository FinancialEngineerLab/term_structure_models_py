import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import math
import statsmodels.api as sm

class CoxIngersoll:
    def __init__(self, time):
        self.yield_data = self.get_yield_data()
        self.a = self.get_mean_revert()
        self.b = self.get_long_term_mean()
        self.t = time 
        self.num_subprocesses = 252*self.t
        self.dt = self.t / self.num_subprocesses 
        self.rates = [self.get_current_rate()]
        self.sigma = self.get_volatility()

    def get_yield_data(self):
        return list(pd.read_excel('DGS10.xls')['DGS10'].fillna(0))

    def get_mean_revert(self):
        lag = np.roll(self.yield_data,1)
        lag[0] = 0
        ret = self.yield_data - lag
        ret[0] = 0
        model = sm.OLS(ret,lag)
        res = model.fit()
        return res.params[0]

    def get_current_rate(self):
        return self.yield_data[-1]
    
    def get_long_term_mean(self):
        # looks back 1 year 
        return np.mean(self.yield_data[-365:])

    def get_volatility(self):
        return np.std(self.yield_data[-30:])
    
    def ci(self):
        for i in range(self.num_subprocesses):
            self.rates.append(self.rates[-1] + (self.b - self.a*self.rates[-1])*self.dt + math.sqrt(self.rates[-1])*self.sigma*np.random.normal())
        return self.rates
    
    def show_rates(self):
        x = range(self.num_subprocesses+1)
        for i in range(100):
            y = self.ci()
            plt.plot(x,y)
            self.rates = [self.get_current_rate()]
        plt.title("Cox-Ingersoll Model")
        plt.show()