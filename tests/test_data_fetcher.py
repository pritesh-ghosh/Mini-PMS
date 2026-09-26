from data.data_fetcher import DataFetcher


def test_fetch_data_returns_market_data_for_default_tickers():
    fetcher = DataFetcher(["RELIANCE.NS", "TCS.NS"], "^NSEI")
    df = fetcher.fetch_data()

    assert not df.empty
    assert len(df.columns) >= 2
    assert "benchmark" in df.columns
