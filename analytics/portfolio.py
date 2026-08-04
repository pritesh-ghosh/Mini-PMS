import pandas as pd
import numpy as np

class PortfolioAnalyzer:
    def __init__(self, returns_data, benchmark_returns, weights):
        self.returns = returns_data
        self.benchmark_returns = benchmark_returns
        self.weights = np.array(weights) / 100
        
    def calculate_portfolio_returns(self):
        """Calculate weighted portfolio returns"""
        return (self.returns * self.weights).sum(axis=1)
    
    def calculate_cagr(self, portfolio_returns):
        """Calculate Compound Annual Growth Rate"""
        total_return = (1 + portfolio_returns).prod() - 1
        years = len(portfolio_returns) / 252
        return (1 + total_return) ** (1 / years) - 1
    
    def calculate_sharpe_ratio(self, portfolio_returns, risk_free_rate=0.05):
        """Calculate Sharpe Ratio"""
        excess_returns = portfolio_returns - risk_free_rate/252
        return np.sqrt(252) * excess_returns.mean() / portfolio_returns.std()
    
    def calculate_sortino_ratio(self, portfolio_returns, risk_free_rate=0.05):
        """Calculate Sortino Ratio"""
        excess_returns = portfolio_returns - risk_free_rate/252
        downside_returns = excess_returns[excess_returns < 0]
        downside_deviation = downside_returns.std()
        return np.sqrt(252) * excess_returns.mean() / downside_deviation if downside_deviation != 0 else 0
    
    def calculate_max_drawdown(self, portfolio_returns):
        """Calculate Maximum Drawdown"""
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    def calculate_beta(self, portfolio_returns):
        """Calculate Beta against benchmark"""
        covariance = np.cov(portfolio_returns, self.benchmark_returns)[0][1]
        benchmark_variance = self.benchmark_returns.var()
        return covariance / benchmark_variance if benchmark_variance != 0 else 0
    
    def calculate_alpha(self, portfolio_returns):
        """Calculate Alpha (Jensen's Alpha)"""
        beta = self.calculate_beta(portfolio_returns)
        portfolio_return = portfolio_returns.mean() * 252
        benchmark_return = self.benchmark_returns.mean() * 252
        risk_free_rate = 0.05
        return portfolio_return - (risk_free_rate + beta * (benchmark_return - risk_free_rate))
    
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