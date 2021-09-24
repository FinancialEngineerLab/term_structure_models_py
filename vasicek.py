import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.optimize import minimize 
import math

class Vasicek:
    def __init__(self, time):
        # get yield data
        self.yield_data = self.get_yield_data()

        # inialize model params 
        self.b = self.get_long_term_avg()
        self.a = 0.01
        self.sigma = self.get_std()

        self.interest_diffs = self.find_interest_rate_diff() 
        self.a, self.b, self.sigma = self.find_params()

        self.t = time 
        self.num_subprocesses = 252*self.t
        self.dt = self.t / self.num_subprocesses 
        self.rates = [self.get_current_rate()]

    def normpdf(self, x, mean, sd):
        var = float(sd)**2
        denom = (2*math.pi*var)**.5
        num = math.exp(-(float(x)-float(mean))**2/(2*var))
        return num/denom

    def minimization_function(self, params):
        modeled_drift = []
        for i in range(1, len(self.interest_diffs) + 1):
            modeled_drift.append(params[0]*(params[1] - (self.yield_data[i-1] / 100)))

        sum_log_normpdf = 0
        for i in range(len(self.interest_diffs)):
            if self.normpdf(self.interest_diffs[i] - modeled_drift[i], 0, params[2]) > 0:
                sum_log_normpdf += math.log(self.normpdf(self.interest_diffs[i] - modeled_drift[i], 0, params[2])) 

        return -1*sum_log_normpdf 
    
    def find_params(self):
        x0 = [self.a, self.b, self.sigma]
        res = minimize(self.minimization_function, x0, method='Nelder-Mead')
        return res['x']

    def get_yield_data(self):
        data = list(pd.read_excel('DGS10.xls')['DGS10'])
        for i in range(len(data)):
            if data[i] == 0:
                data[i] = data[i-1]
        return data
    
    def find_interest_rate_diff(self):
        rates = list(self.yield_data)
        interest_diff = []
        for i in range(1, len(rates)):
            interest_diff.append((rates[i] / 100) - (rates[i-1] / 100))
        return interest_diff 
    
    def get_current_rate(self):
        return self.yield_data[-1]

    def get_long_term_avg(self):
        return np.mean(self.yield_data[-730:])

    def get_std(self):
        return np.std(self.yield_data[-30:])

    def vasicek(self):
        for i in range(self.num_subprocesses):
            self.rates.append(self.rates[-1] + self.a*(self.b-self.rates[-1])*self.dt + self.sigma*np.random.normal())
        return self.rates
    
    def show_rates(self):
        x = range(self.num_subprocesses+1)
        for i in range(100):
            y = self.vasicek()
            plt.plot(x,y)
            self.rates = [self.get_current_rate()]
        plt.title('Vasicek Model')
        plt.show()
