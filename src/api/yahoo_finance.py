# src/api/yahoo_finance.py
import yfinance as yf
import pandas as pd
from typing import Dict

def fetch_yahoo_finance_data(params: Dict[str, str]) -> pd.DataFrame:
    ticker = params["ticker"]
    start_date = params["start_date"]
    end_date = params["end_date"]
    timeframe = params["timeframe"]

    interval = '1d' if timeframe == 'daily' else '1wk' if timeframe == 'weekly' else '1mo'
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date, interval=interval)

    if hist.empty:
        return pd.DataFrame()
    
    hist.reset_index(inplace=True)
    hist['ticker'] = ticker
    hist['timeframe'] = timeframe
    hist = hist.rename(columns={
        'Date': 'date',
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume'
    })
    return hist[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'timeframe']]