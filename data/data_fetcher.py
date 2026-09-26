import requests
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time


class DataFetcher:
    def __init__(self, tickers, benchmark="^NSEI"):
        self.tickers = tickers
        self.benchmark = benchmark
        self.start_date = datetime.now() - timedelta(days=365 * 3)
        self.end_date = datetime.now()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
        })

    def _fetch_via_requests(self, symbol):
        """Fetch chart data directly from Yahoo's public finance endpoint."""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {
            "range": "3y",
            "interval": "1d",
            "includeAdjustedClose": "true"
        }

        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        result = payload.get("chart", {}).get("result") or []
        if not result:
            return pd.DataFrame()

        chart = result[0]
        timestamps = chart.get("timestamp") or []
        indicators = chart.get("indicators", {})
        # Prefer split/dividend-adjusted closes (matches yfinance's default auto_adjust=True)
        adjclose = (indicators.get("adjclose") or [{}])[0].get("adjclose")
        closes = adjclose or (indicators.get("quote") or [{}])[0].get("close") or []

        if not timestamps or not closes or len(closes) < 50:
            return pd.DataFrame()

        series = pd.Series(closes, index=pd.to_datetime(timestamps, unit="s"))
        series = series.dropna().astype(float)
        series.name = symbol
        return series

    def _fetch_via_yfinance(self, symbol):
        """Fallback to yfinance if the direct endpoint is unavailable."""
        stock = yf.Ticker(symbol)
        hist = stock.history(start=self.start_date, end=self.end_date)
        if hist.empty or len(hist) < 50:
            return pd.DataFrame()
        return hist["Close"].rename(symbol)

    def fetch_data(self):
        """Fetch historical data for all tickers and benchmark with resilient error handling."""
        data = {}

        for ticker in self.tickers:
            ticker_found = False
            ticker_variants = [
                ticker,
                ticker + ".NS",
                ticker.upper(),
                ticker.upper() + ".NS",
            ]

            seen = set()
            ticker_variants = [x for x in ticker_variants if not (x in seen or seen.add(x))]

            for variant in ticker_variants:
                try:
                    print(f"Trying {variant}...")
                    series = self._fetch_via_requests(variant)
                    if series.empty:
                        series = self._fetch_via_yfinance(variant)

                    if not series.empty and len(series) > 50:
                        data[ticker] = series
                        print(f"✓ Successfully fetched {ticker} using {variant}")
                        ticker_found = True
                        break
                except Exception as e:
                    print(f"✗ Failed with {variant}: {e}")
                    continue

            if not ticker_found:
                print(f"⚠️ WARNING: Could not fetch data for {ticker}")

        benchmark_found = False
        benchmark_variants = [
            self.benchmark,
            "^NSEI",
            "NIFTY 50",
            "^NSEBANK",
            "^BSESN"
        ]

        for variant in benchmark_variants:
            try:
                print(f"Trying benchmark {variant}...")
                series = self._fetch_via_requests(variant)
                if series.empty:
                    series = self._fetch_via_yfinance(variant)

                if not series.empty and len(series) > 50:
                    data["benchmark"] = series
                    print(f"✓ Successfully fetched benchmark using {variant}")
                    benchmark_found = True
                    break
            except Exception as e:
                print(f"✗ Failed with {variant}: {e}")
                continue

        if not benchmark_found:
            print("⚠️ WARNING: No benchmark data fetched")

        # Align on calendar date: timestamps differ across markets and sources
        # (tz-aware exchange-local from yfinance, naive UTC from the chart endpoint)
        for key, series in data.items():
            idx = series.index.tz_localize(None) if series.index.tz is not None else series.index
            data[key] = series.set_axis(idx.normalize())

        if data:
            df = pd.DataFrame(data).dropna()
            if not df.empty:
                print(f"✓ Successfully fetched data for {len(df.columns)} instruments")
                return df
            raise ValueError("No data after cleaning. Please check your tickers.")

        raise ValueError("No data fetched. Please check your tickers.")