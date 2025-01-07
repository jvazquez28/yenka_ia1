# src/api/alpha_vantage.py
import requests
import pandas as pd
from typing import Dict
import os
import logging

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
logger = logging.getLogger(__name__)

def fetch_alpha_vantage_data(params: Dict[str, str]) -> pd.DataFrame:
    ticker = params["ticker"]
    timeframe = params["timeframe"]
    
    function_mapping = {
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }
    
    function = function_mapping.get(timeframe.lower())
    if not function:
        logger.error(f"Unsupported timeframe: {timeframe}")
        return pd.DataFrame()

    url = (
        f'https://www.alphavantage.co/query?function={function}&symbol={ticker}'
        f'&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=full'
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        time_series_key = next((key for key in data.keys() if "Time Series" in key), None)
        if not time_series_key:
            logger.error("Time Series key not found in API response")
            return pd.DataFrame()

        df = pd.DataFrame.from_dict(data[time_series_key], orient='index').reset_index()
        df.columns = ['bar_date', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']
        df['ticker'] = ticker
        df['timeframe'] = timeframe.lower()
        df['bar_date'] = pd.to_datetime(df['bar_date']).dt.date
        df['bar_time'] = pd.to_datetime('00:00:00').time()  # Default time for daily data

        # Reorder columns to match the database schema
        df = df[['ticker', 'bar_date', 'bar_time', 'timeframe', 'open_price', 'high_price', 'low_price', 'close_price', 'volume']]

        logger.info(f"Fetched {len(df)} records from Alpha Vantage for ticker: {ticker}")
        return df
    else:
        logger.error(f"Failed to fetch data from Alpha Vantage: HTTP {response.status_code}")
        return pd.DataFrame()