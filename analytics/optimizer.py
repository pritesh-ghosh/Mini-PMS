import numpy as np
from scipy.optimize import minimize, Bounds

class PortfolioOptimizer:
    def __init__(self, returns, risk_free_rate=0.05):
        self.returns = returns
        self.risk_free_rate = risk_free_rate
        self.n_assets = len(returns.columns)
        self.mean_returns = returns.mean() * 252
        self.cov_matrix = returns.cov() * 252
        
    def portfolio_performance(self, weights):
        """Calculate return, volatility, and Sharpe for given weights"""
        portfolio_return = np.sum(self.mean_returns * weights)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        sharpe = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        return portfolio_return, portfolio_volatility, sharpe
    
    def negative_sharpe(self, weights):
        """Negative Sharpe for minimization"""
        return -self.portfolio_performance(weights)[2]
    
    def maximize_sharpe_ratio(self):
        """Find weights that maximize Sharpe Ratio"""
        constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        bounds = Bounds(0, 1)
        initial_weights = np.array([1/self.n_assets] * self.n_assets)
        
        result = minimize(self.negative_sharpe, initial_weights,
                         method='SLSQP', bounds=bounds, constraints=constraints)
        
        return result.x if result.success else initial_weights
    
    def efficient_frontier_points(self, n_points=30):
        """Generate points on the efficient frontier"""
        # Get min and max returns
        min_return = self.mean_returns.min()
        max_return = self.mean_returns.max()
        
        target_returns = np.linspace(min_return, max_return, n_points)
        volatilities = []
        returns_list = []
        
        for target in target_returns:
            constraints = (
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: np.sum(self.mean_returns * x) - target}
            )
            bounds = Bounds(0, 1)
            
            result = minimize(lambda x: np.sqrt(np.dot(x.T, np.dot(self.cov_matrix, x))),
                            np.array([1/self.n_assets] * self.n_assets),
                            method='SLSQP', bounds=bounds, constraints=constraints)
            
            if result.success:
                volatilities.append(np.sqrt(np.dot(result.x.T, np.dot(self.cov_matrix, result.x))))
                returns_list.append(target)
        
        return returns_list, volatilities