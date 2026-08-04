import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

class DataFetcher:
    def __init__(self, tickers, benchmark="^NSEI"):
        self.tickers = tickers
        self.benchmark = benchmark
        self.start_date = datetime.now() - timedelta(days=365*3)
        self.end_date = datetime.now()
        
    def fetch_data(self):
        """Fetch historical data for all tickers and benchmark with better error handling"""
        data = {}
        
        # Try different ticker formats
        for ticker in self.tickers:
            ticker_found = False
            ticker_variants = [
                ticker,  # Original
                ticker.replace('.NS', ''),  # Without .NS
                ticker + '.NS',  # With .NS
                ticker.upper(),  # Uppercase
                ticker.upper() + '.NS',  # Uppercase with .NS
            ]
            
            # Remove duplicates while preserving order
            seen = set()
            ticker_variants = [x for x in ticker_variants if not (x in seen or seen.add(x))]
            
            for variant in ticker_variants:
                try:
                    print(f"Trying {variant}...")
                    stock = yf.Ticker(variant)
                    hist = stock.history(start=self.start_date, end=self.end_date)
                    
                    if not hist.empty and len(hist) > 50:  # Need enough data points
                        data[ticker] = hist['Close']
                        print(f"✓ Successfully fetched {ticker} using {variant}")
                        ticker_found = True
                        break
                except Exception as e:
                    print(f"✗ Failed with {variant}: {e}")
                    continue
            
            if not ticker_found:
                print(f"⚠️ WARNING: Could not fetch data for {ticker}")
                # Try with a fallback to a known working ticker for demo
                if 'RELIANCE' in ticker or 'RELIANCE.NS' in ticker:
                    print("Using RELIANCE.NS as fallback...")
                    try:
                        stock = yf.Ticker("RELIANCE.NS")
                        hist = stock.history(start=self.start_date, end=self.end_date)
                        if not hist.empty:
                            data[ticker] = hist['Close']
                            print("✓ Fallback successful")
                    except:
                        pass
        
        # Fetch benchmark data with fallback
        benchmark_found = False
        benchmark_variants = [
            self.benchmark,
            '^NSEI',
            'NIFTY 50',
            '^NSEBANK',
            '^BSESN'
        ]
        
        for variant in benchmark_variants:
            try:
                print(f"Trying benchmark {variant}...")
                benchmark_stock = yf.Ticker(variant)
                benchmark_hist = benchmark_stock.history(start=self.start_date, end=self.end_date)
                if not benchmark_hist.empty and len(benchmark_hist) > 50:
                    data['benchmark'] = benchmark_hist['Close']
                    print(f"✓ Successfully fetched benchmark using {variant}")
                    benchmark_found = True
                    break
            except Exception as e:
                print(f"✗ Failed with {variant}: {e}")
                continue
        
        if not benchmark_found:
            print("⚠️ WARNING: No benchmark data fetched")
        
        # Create DataFrame
        if data:
            df = pd.DataFrame(data).dropna()
            if not df.empty:
                print(f"✓ Successfully fetched data for {len(df.columns)} instruments")
                return df
            else:
                raise ValueError("No data after cleaning. Please check your tickers.")
        else:
            raise ValueError("No data fetched. Please check your tickers.")