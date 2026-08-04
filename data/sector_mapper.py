import yfinance as yf

class SectorMapper:
    def __init__(self):
        self.sector_cache = {}
        
    def get_sector(self, ticker):
        """Fetch sector information using Yahoo Finance"""
        if ticker in self.sector_cache:
            return self.sector_cache[ticker]
        
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            sector = info.get('sector', 'Unknown')
            
            if not sector or sector == 'Unknown':
                # Fallback to industry
                sector = info.get('industry', 'Other')
            
            self.sector_cache[ticker] = sector
            return sector
            
        except Exception as e:
            print(f"Error fetching sector for {ticker}: {e}")
            return 'Other'
    
    def get_sector_allocation(self, tickers, weights):
        """Get sector allocation for a portfolio"""
        sector_weights = {}
        
        for ticker, weight in zip(tickers, weights):
            sector = self.get_sector(ticker)
            sector_weights[sector] = sector_weights.get(sector, 0) + weight
        
        return sector_weights