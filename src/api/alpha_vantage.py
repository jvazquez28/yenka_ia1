# src/api/alpha_vantage.py
import requests
import pandas as pd
from typing import Dict
import os

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def fetch_alpha_vantage_data(params: Dict[str, str]) -> pd.DataFrame:
    ticker = params["ticker"]
    timeframe = params["timeframe"]
    function = "TIME_SERIES_DAILY" if timeframe == "daily" else "TIME_SERIES_WEEKLY" if timeframe == "weekly" else "TIME_SERIES_MONTHLY"
    url = f'https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series_key = next(key for key in data.keys() if "Time Series" in key)
        df = pd.DataFrame.from_dict(data[time_series_key], orient='index').reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        df['ticker'] = ticker
        df['timeframe'] = timeframe
        df['date'] = pd.to_datetime(df['date']).dt.date
        return df[['ticker', 'date', 'open', 'high', 'low', 'close', 'volume', 'timeframe']]
    else:
        return pd.DataFrame()