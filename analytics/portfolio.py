import pandas as pd
import numpy as np

class PortfolioAnalyzer:
    def __init__(self, returns_data, benchmark_returns, weights, risk_free_rate=0.05):
        self.returns = returns_data
        self.benchmark_returns = benchmark_returns
        self.weights = np.array(weights) / 100
        self.risk_free_rate = risk_free_rate
        
    def calculate_portfolio_returns(self):
        """Calculate weighted portfolio returns"""
        return (self.returns * self.weights).sum(axis=1)
    
    def calculate_cagr(self, portfolio_returns):
        """Calculate Compound Annual Growth Rate"""
        total_return = (1 + portfolio_returns).prod() - 1
        years = len(portfolio_returns) / 252
        return (1 + total_return) ** (1 / years) - 1
    
    def calculate_sharpe_ratio(self, portfolio_returns):
        """Calculate Sharpe Ratio"""
        excess_returns = portfolio_returns - self.risk_free_rate/252
        return np.sqrt(252) * excess_returns.mean() / portfolio_returns.std()
    
    def calculate_sortino_ratio(self, portfolio_returns):
        """Calculate Sortino Ratio"""
        excess_returns = portfolio_returns - self.risk_free_rate/252
        # Downside deviation: RMS of below-target returns over ALL periods (not std of the negative subset)
        downside_deviation = np.sqrt((np.minimum(excess_returns, 0) ** 2).mean())
        return np.sqrt(252) * excess_returns.mean() / downside_deviation if downside_deviation != 0 else 0
    
    def calculate_max_drawdown(self, portfolio_returns):
        """Calculate Maximum Drawdown"""
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def calculate_beta(self, portfolio_returns):
        """Calculate Beta against benchmark"""
        if self.benchmark_returns is None:
            return None
        covariance = np.cov(portfolio_returns, self.benchmark_returns)[0][1]
        benchmark_variance = self.benchmark_returns.var()
        return covariance / benchmark_variance if benchmark_variance != 0 else 0
    
    def calculate_alpha(self, portfolio_returns):
        """Calculate Alpha (Jensen's Alpha)"""
        beta = self.calculate_beta(portfolio_returns)
        if beta is None:
            return None
        portfolio_return = portfolio_returns.mean() * 252
        benchmark_return = self.benchmark_returns.mean() * 252
        return portfolio_return - (self.risk_free_rate + beta * (benchmark_return - self.risk_free_rate))
    
    def calculate_volatility(self, portfolio_returns):
        """Calculate Annualized Volatility"""
        return portfolio_returns.std() * np.sqrt(252)
    
    def get_all_metrics(self, portfolio_returns):
        """Calculate all portfolio metrics"""
        metrics = {
            'Total Return': (1 + portfolio_returns).prod() - 1,
            'CAGR': self.calculate_cagr(portfolio_returns),
            'Annualized Return': portfolio_returns.mean() * 252,
            'Annualized Volatility': self.calculate_volatility(portfolio_returns),
            'Sharpe Ratio': self.calculate_sharpe_ratio(portfolio_returns),
            'Sortino Ratio': self.calculate_sortino_ratio(portfolio_returns),
            'Max Drawdown': self.calculate_max_drawdown(portfolio_returns),
            'Beta': self.calculate_beta(portfolio_returns),
            'Alpha': self.calculate_alpha(portfolio_returns)
        }
        return metrics