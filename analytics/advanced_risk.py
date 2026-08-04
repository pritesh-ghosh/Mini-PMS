import numpy as np
from scipy import stats

class AdvancedRiskMetrics:
    def __init__(self, returns, benchmark_returns=None):
        self.returns = returns
        self.benchmark = benchmark_returns
        
    def calculate_omega_ratio(self, portfolio_returns, threshold=0):
        """Omega Ratio - considers all moments of distribution"""
        returns_above = portfolio_returns[portfolio_returns > threshold]
        returns_below = portfolio_returns[portfolio_returns <= threshold]
        
        if len(returns_below) == 0:
            return np.inf
        
        gain = np.sum(returns_above - threshold)
        loss = np.sum(threshold - returns_below)
        
        return gain / loss if loss != 0 else np.inf
    
    def calculate_calmar_ratio(self, portfolio_returns):
        """Calmar Ratio - return per unit of maximum drawdown"""
        cumulative = (1 + portfolio_returns).cumprod()
        max_drawdown = self.calculate_max_drawdown(portfolio_returns)
        annual_return = (1 + portfolio_returns).prod() ** (252/len(portfolio_returns)) - 1
        return annual_return / abs(max_drawdown) if max_drawdown != 0 else 0
    
    def calculate_max_drawdown(self, portfolio_returns):
        """Calculate Maximum Drawdown"""
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def calculate_ulcer_index(self, portfolio_returns):
        """Ulcer Index - measures downside risk"""
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown_pct = (cumulative - running_max) / running_max * 100
        
        squared_drawdowns = drawdown_pct ** 2
        ulcer_index = np.sqrt(squared_drawdowns.mean())
        return ulcer_index
    
    def calculate_skewness(self, portfolio_returns):
        """Return skewness"""
        return stats.skew(portfolio_returns)
    
    def calculate_kurtosis(self, portfolio_returns):
        """Return kurtosis"""
        return stats.kurtosis(portfolio_returns)