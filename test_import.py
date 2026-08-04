# test_imports.py
print("Testing imports...")

try:
    from analytics.portfolio import PortfolioAnalyzer
    print("✓ PortfolioAnalyzer imported")
except Exception as e:
    print(f"✗ PortfolioAnalyzer failed: {e}")

try:
    from data.data_fetcher import DataFetcher
    print("✓ DataFetcher imported")
except Exception as e:
    print(f"✗ DataFetcher failed: {e}")

print("Done!")