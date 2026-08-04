class RecommendationEngine:
    def __init__(self, portfolio_metrics, health_score, sector_allocation):
        self.metrics = portfolio_metrics
        self.health = health_score
        self.sector_allocation = sector_allocation
        
    def generate_recommendations(self):
        """Generate personalized portfolio recommendations"""
        recommendations = []
        
        # 1. Sector concentration check
        if self.sector_allocation:
            max_sector = max(self.sector_allocation.items(), key=lambda x: x[1])
            if max_sector[1] > 40:
                recommendations.append({
                    'type': '⚠️ Sector Concentration',
                    'title': f'High {max_sector[0]} Exposure',
                    'detail': f'Your portfolio has {max_sector[1]:.1f}% in {max_sector[0]}, above recommended 40%.',
                    'action': 'Consider diversifying by adding stocks from other sectors or sector-specific ETFs.',
                    'severity': 'high'
                })
        
        # 2. Sharpe Ratio check
        if self.metrics['Sharpe Ratio'] < 1.0:
            recommendations.append({
                'type': '📊 Risk-Adjusted Returns',
                'title': 'Suboptimal Sharpe Ratio',
                'detail': f'Your Sharpe Ratio is {self.metrics["Sharpe Ratio"]:.2f}, below target of 1.0.',
                'action': 'Portfolio not delivering sufficient return for risk level. Consider adding bonds or defensive stocks.',
                'severity': 'medium'
            })
        
        # 3. Volatility check
        if self.metrics['Annualized Volatility'] > 0.25:
            recommendations.append({
                'type': '⚡ High Volatility',
                'title': 'Elevated Portfolio Volatility',
                'detail': f'Annualized volatility is {self.metrics["Annualized Volatility"]*100:.1f}%.',
                'action': 'Reduce concentration in high-beta stocks. Consider adding low-volatility stocks.',
                'severity': 'high'
            })
        
        # 4. Max Drawdown check
        if abs(self.metrics['Max Drawdown']) > 0.35:
            recommendations.append({
                'type': '🔻 Downside Risk',
                'title': 'Significant Maximum Drawdown',
                'detail': f'Portfolio experienced {abs(self.metrics["Max Drawdown"])*100:.1f}% drawdown.',
                'action': 'Add defensive positions (gold, bonds, consumer staples) to cushion against market downturns.',
                'severity': 'high'
            })
        
        # 5. Overall Health check
        if self.health['score'] < 60:
            recommendations.append({
                'type': '💊 Portfolio Health',
                'title': 'Portfolio Needs Improvement',
                'detail': f'Health score is {self.health["score"]}/100.',
                'action': 'Review individual component scores (diversification, volatility, concentration) and address weakest areas.',
                'severity': 'medium'
            })
        
        # If no issues, positive recommendation
        if not recommendations:
            recommendations.append({
                'type': '✅ Portfolio Health',
                'title': 'Well-Diversified Portfolio',
                'detail': 'Your portfolio shows good diversification and risk management.',
                'action': 'Continue to monitor allocations quarterly and rebalance to maintain target weights.',
                'severity': 'low'
            })
            
        return recommendations