import yfinance as yf

# Test different formats
test_tickers = ["RELIANCE.NS", "RELIANCE", "TCS.NS", "TCS", "HDFCBANK.NS", "HDFC"]

for ticker in test_tickers:
    try:
        print(f"\nTesting: {ticker}")
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        if not hist.empty:
            print(f"✓ SUCCESS: {ticker} works! Latest close: ${hist['Close'].iloc[-1]:.2f}")
        else:
            print(f"✗ FAILED: {ticker} returned empty data")
    except Exception as e:
        print(f"✗ ERROR: {ticker} - {str(e)[:50]}")