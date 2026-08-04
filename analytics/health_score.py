class HealthScoreCalculator:
    def __init__(self, metrics, weights, sector_allocation):
        self.metrics = metrics
        self.weights = weights
        self.sector_allocation = sector_allocation
        
    def calculate_diversification_score(self):
        """Score based on number of stocks and sector distribution"""
        hhi = sum([(w/100)**2 for w in self.weights])
        
        if hhi < 0.15:
            return 95
        elif hhi < 0.25:
            return 80
        elif hhi < 0.35:
            return 65
        elif hhi < 0.50:
            return 45
        else:
            return 25
            
    def calculate_volatility_score(self):
        """Score based on annualized volatility"""
        vol = self.metrics['Annualized Volatility']
        
        if vol < 0.15:
            return 90
        elif vol < 0.20:
            return 75
        elif vol < 0.25:
            return 60
        elif vol < 0.30:
            return 45
        else:
            return 25
            
    def calculate_concentration_score(self):
        """Score based on portfolio concentration"""
        max_weight = max(self.weights)
        top3_sum = sum(sorted(self.weights, reverse=True)[:3])
        
        if max_weight < 20 and top3_sum < 40:
            return 95
        elif max_weight < 25 and top3_sum < 50:
            return 80
        elif max_weight < 30 and top3_sum < 60:
            return 65
        elif max_weight < 40 and top3_sum < 70:
            return 45
        else:
            return 25
            
    def calculate_drawdown_score(self):
        """Score based on maximum drawdown"""
        drawdown = abs(self.metrics['Max Drawdown'])
        
        if drawdown < 0.10:
            return 90
        elif drawdown < 0.20:
            return 75
        elif drawdown < 0.30:
            return 60
        elif drawdown < 0.40:
            return 40
        else:
            return 20
            
    def calculate_performance_score(self):
        """Score based on risk-adjusted returns"""
        sharpe = self.metrics['Sharpe Ratio']
        
        if sharpe > 2.0:
            return 95
        elif sharpe > 1.5:
            return 80
        elif sharpe > 1.0:
            return 65
        elif sharpe > 0.5:
            return 45
        else:
            return 25
            
    def get_health_score(self):
        """Calculate overall health score out of 100"""
        scores = {
            'Diversification': self.calculate_diversification_score(),
            'Volatility': self.calculate_volatility_score(),
            'Concentration': self.calculate_concentration_score(),
            'Drawdown': self.calculate_drawdown_score(),
            'Performance': self.calculate_performance_score()
        }
        
        weights = {
            'Diversification': 0.30,
            'Volatility': 0.25,
            'Concentration': 0.20,
            'Drawdown': 0.15,
            'Performance': 0.10
        }
        
        total_score = sum(scores[key] * weights[key] for key in scores)
        
        if total_score >= 80:
            rating = "Excellent"
        elif total_score >= 65:
            rating = "Good"
        elif total_score >= 50:
            rating = "Fair"
        elif total_score >= 35:
            rating = "Needs Improvement"
        else:
            rating = "High Risk"
            
        return {
            'score': round(total_score, 1),
            'rating': rating,
            'breakdown': scores
        }